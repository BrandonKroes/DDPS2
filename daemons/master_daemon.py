import multiprocessing
import pickle
import sys
import sqlite3
from sqlite3 import Error

from common.cron.cron_worker_manager import CronWorkerManager
from daemons import OperatorDaemon, OperatorTypes
from common.communication import ReceiveSocket, SendSocket
from common.packets import JobType, AbstractPacket
from common.parser import YAMLParser
from master.classes.packet_router import PacketRouter
from master.operations import OperationManager
from urllib.request import pathname2url


class MasterDaemon(OperatorDaemon):
    active = True
    cron = []  # time sensitive operations
    workers = []
    db = None  # the DB conn
    db_filename = "master_db.db"

    def __init__(self, config_path):
        super().__init__(OperatorTypes.MASTER)

        if self.if_database_exits():
            self.import_db()
        else:
            self.initialize_db()

        self.conf = YAMLParser.PathToDict(config_path)
        self.incoming_request, incoming_request_pipe = multiprocessing.Pipe(duplex=True)

        self.operations_manager = OperationManager()

        self.outgoing_request, outgoing_request_pipe = multiprocessing.Pipe(duplex=True)

        self.listening_pipes = [self.incoming_request]

        self.listen_sockets = [
            multiprocessing.Process(target=ReceiveSocket, args=((incoming_request_pipe, self.conf['master']),))
        ]
        self.outgoing_sockets = [
            multiprocessing.Process(target=SendSocket, args=(outgoing_request_pipe,))
        ]

        self.packet_router = PacketRouter()

        # start all sockets
        for x in self.listen_sockets + self.outgoing_sockets:
            x.start()

    def boot(self):
        self.cron.append(CronWorkerManager())

    # Source: https://stackoverflow.com/questions/12932607/how-to-check-if-a-sqlite3-database-exists-in-python
    def if_database_exits(self):

        from os.path import isfile, getsize

        if not isfile(self.db_filename):
            return False
        if getsize(self.db_filename) < 100:  # SQLite database file header is 100 bytes
            return False

        with open(self.db_filename, 'rb') as fd:
            header = fd.read(100)

        return header[:16] == 'SQLite format 3\x00'

    def initialize_db(self):
        try:
            self.db = sqlite3.connect(self.db_filename)
            db_query = """ CREATE TABLE IF NOT EXISTS master_state (
                                        id integer PRIMARY KEY,
                                        content BLOB
                                    ); """
            self.db.execute(db_query)
        except Error as e:
            print(e)

    def import_db(self):
        query = '''SELECT *
                    FROM master_state
                    ORDER BY id DESC
                    LIMIT 1'''
        self.db.execute(query)
        db_recovery = pickle.loads(self.db.cursor().fetchone())
        self.workers = db_recovery['workers']
        self.operations_manager = db_recovery['operations_manager']

    def export_status(self):
        query = '''INSERT INTO master_state(content)
              VALUES(?)'''

        self.db.execute(query, pickle.dumps(self.__dict__))

    def check_for_cron(self):
        for cron_operation in self.cron:
            cron_operation.cron_time_passed_master(self)

    def check_listen_sockets(self) -> ['AbstractPacket']:
        to_process: ['AbstractPacket'] = []
        for listen_socket in self.listening_pipes:
            if listen_socket.poll():
                to_process.append(listen_socket.recv().packet)
        return to_process

    def send_packet(self, endpoint):
        self.outgoing_request.send(endpoint)

    def main(self):
        # TODO: KeyboardInterrupt to shutdown systems!

        while self.active:
            self.check_for_cron()
            packet_queue = self.check_listen_sockets()
            for packet in packet_queue:
                self.packet_router.new_packet(self, packet)

    def register_node_failure(self, node):
        # check if the node is part of an operation
        self.operations_manager.report_node_failure(master=self, node=node)

    def delete_database(self):
        import os
        os.remove(self.db_filename)

    def shutdown(self):
        self.delete_database()
        print("Goodbye!")
        sys.exit()

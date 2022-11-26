# new clients
# new tasks
# status
# merging
# assigning tasks
# file management
# user input
# reschedule
# failsafe
import multiprocessing

from common.communication.sockets.receive_socket import ReceiveSocket
from common.communication.sockets.send_socket import SendSocket
from common.operator import *
from common.packets.abstract_packet import AbstractPacket
from common.parser.yaml_parser import YAMLParser


class MasterDaemon(Operator):
    active = True
    cron = []  # time sensitive operations
    workers = []

    def __init__(self, config_path):
        super().__init__(OperatorTypes.MASTER)
        self.conf = YAMLParser.PathToDict(config_path)
        self.incoming_request, incoming_request_pipe = multiprocessing.Pipe(duplex=True)

        self.outgoing_request, outgoing_request_pipe = multiprocessing.Pipe(duplex=True)

        self.listening_pipes = [self.incoming_request]

        self.listen_sockets = [
            multiprocessing.Process(target=ReceiveSocket, args=((incoming_request_pipe, self.conf['master']),))
        ]
        self.outgoing_sockets = [
            multiprocessing.Process(target=SendSocket, args=(outgoing_request_pipe,))
        ]

        # start all sockets
        for x in self.listen_sockets + self.outgoing_sockets:
            x.start()

    def check_listen_sockets(self):
        to_process = []
        for listen_socket in self.listening_pipes:
            if listen_socket.poll():
                to_process.append(listen_socket.recv())
        return to_process

    def process_packet_operation(self, packet: AbstractPacket):
        packet.execute_master_side(self)

    def main(self):
        while self.active:
            operations = self.check_listen_sockets()
            for operation in operations:
                self.process_packet_operation(operation)


if __name__ == "__main__":
    MasterDaemon("../config/conf.yaml")

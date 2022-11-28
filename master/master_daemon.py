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
import sys
from common.communication.sockets.receive_socket import ReceiveSocket
from common.communication.sockets.send_socket import SendSocket
from common.operator import *
from common.packets.abstract_packet import AbstractPacket
from common.packets.jobtype import JobType
from common.parser.yaml_parser import YAMLParser
from master.operations.blender_operation import BlenderOperation
from master.operations.operation_manager import OperationManager


class MasterDaemon(Operator):
    active = True
    cron = []  # time sensitive operations
    workers = []

    def __init__(self, config_path):
        super().__init__(OperatorTypes.MASTER)
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

        # start all sockets
        for x in self.listen_sockets + self.outgoing_sockets:
            x.start()

    def check_listen_sockets(self) -> [AbstractPacket]:
        to_process: [AbstractPacket] = []
        for listen_socket in self.listening_pipes:
            if listen_socket.poll():
                to_process.append(listen_socket.recv().packet)
        return to_process

    def process_packet_operation(self, packet: AbstractPacket):
        if packet.job_type == JobType.OPERATION:
            self.operations_manager.instantiate_job(data_packet=packet, master=self)
        else:
            packet.execute_master_side(self)

    def send_packet(self, endpoint):
        self.outgoing_request.send(endpoint)

    def main(self):
        while self.active:
            operations = self.check_listen_sockets()
            if len(operations) > 0:
                for operation in operations:
                    try:
                        operation.print()
                    except TypeError:
                        print("Type lacks a print function")
                    self.process_packet_operation(operation)
            self.operations_manager.main(self)

    def shutdown(self):
        print("Goodbye!")
        sys.exit()

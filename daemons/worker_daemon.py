import multiprocessing
from multiprocessing import Process

from daemons import OperatorDaemon, OperatorTypes
from common.communication import ReceiveSocket, SendSocket, EndpointConfig
from common.packets import RegisterClient
from common.packets.job_type import JobType
from common.parser.yaml_parser import YAMLParser


class WorkerDaemon(OperatorDaemon):
    blender_path = ""
    active_packet = None
    actively_working = False
    activated = False
    scheduled_jobs = []
    active_processes = []

    idle = True

    def __init__(self, config_path):
        super().__init__(OperatorTypes.WORKER)
        self.conf = YAMLParser.PathToDict(config_path)
        self.blender_path = self.conf['worker']['blender_path']
        self.worker_id = 0
        self.worker_host = self.conf['worker']['host']
        self.worker_port = self.conf['worker']['port']

        self.master_host = self.conf['master']['host']
        self.master_port = self.conf['master']['port']

        self.incoming_request, incoming_request_pipe = multiprocessing.Pipe(duplex=True)

        self.outgoing_request, outgoing_request_pipe = multiprocessing.Pipe(duplex=True)

        self.listening_pipes = [self.incoming_request]

        self.listen_sockets = [
            multiprocessing.Process(target=ReceiveSocket, args=((incoming_request_pipe, self.conf['worker']),))
        ]

        self.outgoing_sockets = [
            multiprocessing.Process(target=SendSocket, args=(outgoing_request_pipe,))
        ]

        # start all sockets
        for x in self.listen_sockets + self.outgoing_sockets:
            x.start()

    def boot(self):
        # Register with master
        self.send_packet(
            EndpointConfig(host=self.master_host, port=self.master_port,
                           packet=RegisterClient(data_packet=self.conf, packet_id=0, job_type=JobType.REGISTER)))

    def execute_new_job(self):
        self.actively_working = True
        self.active_packet = self.scheduled_jobs.pop()
        p = Process(target=self.active_packet.execute_worker_side, args=(self,))
        p.start()
        self.active_processes.append(p)

    def not_performing_job_but_job_queued(self):
        return self.actively_working is False and len(self.scheduled_jobs) > 0

    def check_if_active_processes_done(self):
        for active_process in self.active_processes[:]:
            if active_process.exitcode is 0:
                self.active_processes.remove(active_process)

    def send_packet(self, endpoint):
        self.outgoing_request.send(endpoint)

    def main(self):
        while True:
            # update incoming sockets
            # self.check_if_active_processes_done()
            # if self.not_performing_job_but_job_queued():
            if len(self.scheduled_jobs) > 0:
                self.execute_new_job()

            operations = self.check_listen_sockets()

            if len(operations) > 0:
                print("received new job")
                for operation in operations:
                    self.add_scheduled_job(operation)

            # queue incoming jobs for schedule

    def check_listen_sockets(self) -> ['AbstractPacket']:
        to_process: ['AbstractPacket'] = []
        for listen_socket in self.listening_pipes:
            if listen_socket.poll():
                ap = listen_socket.recv()
                to_process.append(ap.packet)
        return to_process

    def add_scheduled_job(self, packet: 'AbstractPacket'):
        self.scheduled_jobs.append(packet)
        return

    def shutdown(self):
        self.outgoing_request.close()
        self.incoming_request.close()
        quit()

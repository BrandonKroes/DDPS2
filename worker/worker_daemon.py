import multiprocessing

from common.communication.endpoint_config import EndpointConfig
from common.communication.sockets.receive_socket import ReceiveSocket
from common.communication.sockets.send_socket import SendSocket
from common.operator import Operator, OperatorTypes
from common.packets.abstract_packet import AbstractPacket
from common.packets.jobs import JobType
from common.packets.register_client import RegisterClient
from common.parser.yaml_parser import YAMLParser

from worker.tasks.task_blender import TaskBlender as Blender
from multiprocessing import Process


class WorkerDaemon(Operator):
    blender_path = ""
    output_folder = "/home/brand/lu/ddps/assignment2/example/"
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

        self.worker_host = self.conf['master']['host']
        self.worker_port = self.conf['master']['port']

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

    def boot(self):
        # Register with master
        self.outgoing_request.send(
            EndpointConfig(host=self.master_host, port=self.master_port,
                           packet=RegisterClient(data_packet=self, packet_id=0, job_type=JobType.REGISTER)))

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
            self.check_if_active_processes_done()
            if self.not_performing_job_but_job_queued():
                self.execute_new_job()

    def add_scheduled_job(self, packet: AbstractPacket):
        self.scheduled_jobs.append(packet)

    def execute_render(self, job_content):
        job_content['blender_path'] = self.blender_path
        jb = Blender(**job_content)
        jb.execute()
        self.actively_working = False


if __name__ == "__main__":
    wd = WorkerDaemon()
    wd.boot()
    wd.main()

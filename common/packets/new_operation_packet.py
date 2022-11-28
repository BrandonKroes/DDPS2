from common.communication.endpoint_config import EndpointConfig
from common.packets.abstract_packet import AbstractPacket
from common.packets.jobtype import JobType
from worker.worker_daemon import WorkerDaemon


class NewOperationPacket(AbstractPacket):
    packet_id = None
    boot = True

    def __init__(self, packet_id, job_type, data_packet):
        super().__init__(packet_id, job_type, data_packet)

    def execute_worker_side(self, worker: 'WorkerDaemon'):
        # if it's in the worker, we need to send it to the master!
        worker.send_packet(
            EndpointConfig(host=worker.master_host,
                           port=worker.master_port,
                           packet=self.data_packet))

from common.packets import AbstractPacket
from .job_type import JobType as JobType
import time


class HeartBeatPacket(AbstractPacket):
    packet_id = None

    def __init__(self, packet_id, job_type, data_packet):
        super().__init__(packet_id, job_type, data_packet)

    def execute_master_side(self, master):
        workers = []
        for (node, status) in master.workers:
            if status['worker_id'] == self.data_packet:
                status['last_message'] = time.time() + 10
                status['attempt'] = 0
            workers.append((node, status))
        master.workers = workers

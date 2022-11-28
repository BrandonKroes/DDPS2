from common.packets.abstract_packet import AbstractPacket


class WorkerStatusPacket(AbstractPacket):

    def __init__(self, packet_id, job_type, data_packet):
        super().__init__(packet_id, job_type, data_packet)

    def execute_worker_side(self, worker):
        pass

    def execute_master_side(self, master):
        pass

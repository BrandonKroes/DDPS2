from common.packets import AbstractPacket
from .job_type import JobType as JobType


class HeartBeatPacket(AbstractPacket):
    packet_id = None

    def __init__(self, packet_id, job_type, data_packet):
        super().__init__(packet_id, job_type, data_packet)

    def execute_master_side(self, master):
        # master initiates sending it to the client.
        # after boot the master needs to accept it as done
        # pass
        print("heartbeat update")

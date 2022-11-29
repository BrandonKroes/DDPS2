from abc import ABC
from typing import TYPE_CHECKING
from common.packets.job_type import JobType

if TYPE_CHECKING:
    from DaemonOperators.worker_daemon import WorkerDaemon
    from DaemonOperators.master_daemon import MasterDaemon


class AbstractPacket(ABC):
    packet_id = ""
    data_packet = ""

    def __init__(self, packet_id, job_type: 'JobType', data_packet):
        self.packet_id = packet_id
        self.job_type = job_type
        self.data_packet = data_packet

    def get_id(self):
        return self.packet_id

    def print(self):
        print("PacketID = " + str(self.packet_id) + " | JobType = " + str(self.job_type.name))

    def get_data_packet(self):
        return self.data_packet

    def get_type(self):
        return self.job_type

    def execute_master_side(self, operator: 'MasterDaemon'):
        pass

    def close(self):
        pass

    def execute_worker_side(self, operator: 'WorkerDaemon'):
        pass

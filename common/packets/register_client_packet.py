import time

from common.communication import EndpointConfig
from common.packets import AbstractPacket, WorkerIDPacket
from .job_type import JobType


class RegisterClient(AbstractPacket):

    def __init__(self, packet_id, job_type, data_packet):
        super().__init__(packet_id, job_type, data_packet)

    def execute_master_side(self, master: 'MasterDaemon'):
        # try:
        worker_id = len(master.workers)
        self.get_data_packet()['worker_id'] = worker_id
        master.workers.append(
            (self.get_data_packet(), dict({'worker_id': worker_id, 'last_message': time.time(), 'attempt': 0})))

        print("Added new worker, workerID = " + str(worker_id))

        master.send_packet(
            EndpointConfig(host=self.get_data_packet()['worker']['host'],
                           port=self.get_data_packet()['worker']['port'],
                           packet=WorkerIDPacket(packet_id=0, job_type=JobType.REGISTER, data_packet=worker_id)))
    # except Exception:
    #    print("Exception with packet_id " + str(self.packet_id))

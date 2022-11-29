from common.communication.endpoint_config import EndpointConfig
from common.packets.abstract_packet import AbstractPacket
from common.packets.jobtype import JobType
from common.packets.worker_id_packet import WorkerIDPacket


class RegisterClient(AbstractPacket):

    def __init__(self, packet_id, job_type, data_packet):
        super().__init__(packet_id, job_type, data_packet)

    def execute_master_side(self, master: 'MasterDaemon'):
        # try:
        worker_id = len(master.workers)
        self.get_data_packet()['worker_id'] = worker_id
        master.workers.append(self.get_data_packet())

        print("Added new worker, workerID = " + str(worker_id))

        master.send_packet(
            EndpointConfig(host=self.get_data_packet()['worker']['host'],
                           port=self.get_data_packet()['worker']['port'],
                           packet=WorkerIDPacket(0, JobType.REGISTER, worker_id)))
    # except Exception:
    #    print("Exception with packet_id " + str(self.packet_id))

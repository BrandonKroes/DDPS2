from common.communication.endpoint_config import EndpointConfig
from common.packets.abstract_packet import AbstractPacket
from master.master_daemon import MasterDaemon


class RegisterClient(AbstractPacket):

    def __init__(self, packet_id, job_type, data_packet):
        super().__init__(packet_id, job_type, data_packet)

    def execute_master_side(self, master: MasterDaemon):
        master.workers.append(self.get_data_packet())
        master.outgoing_request(
            EndpointConfig(host=self.get_data_packet().worker_host, port=self.get_data_packet().worker_port,
                           packet=self.get_data_packet()))

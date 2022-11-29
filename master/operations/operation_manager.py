from common.packets.jobtype import JobType
from master.operations.blender_operation import BlenderOperation


class OperationManager:
    operations = []
    operation_count = 0

    def __init__(self):
        pass

    def instantiate_job(self, data_packet, master):
        self.operation_count += 1
        data_packet.operation_id = self.operation_count
        data_packet.orchestrate_cluster(nodes=master.workers)
        for packet in data_packet.get_packets():
            print(packet.__dict__)
            master.send_packet(packet)

    def main(self, master):
        pass

from common.packets.job_type import JobType
from master.operations.blender_operation import BlenderOperation


class OperationManager:
    operations = []
    operation_count = 0

    def __init__(self):
        pass

    def instantiate_operation(self, data_packet, master):
        self.operation_count += 1
        data_packet.operation_id = self.operation_count
        data_packet.orchestrate_cluster(nodes=master.workers)
        for packet in data_packet.get_packets():
            # TODO: log operation activation
            master.send_packet(packet)
            print("sending out packets")
        self.operations.append(data_packet)

    def operation_callback(self, master, data_packet):
        for operation in self.operations:
            print("====")
            print(operation)
            print(data_packet)

            if operation.operation_id == data_packet['operation_reference']:
                operation.process_progress_packet(data_packet)

    def main(self, master):
        pass

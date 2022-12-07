from common.packets.job_type import JobType
from master.operations.blender_operation import BlenderOperation


class OperationManager:
    operations = []
    operation_count = 0

    def __init__(self):
        pass

    def report_node_failure(self, master, node):
        for operation in self.operations:
            operation.node_failure(master=master, failure_node=node)

    def instantiate_operation(self, master, data_packet):
        self.operation_count += 1
        data_packet.operation_id = self.operation_count
        data_packet.orchestrate_cluster(nodes=master.workers)
        for packet in data_packet.get_packets():
            # TODO: log operation activation
            master.send_packet(packet)
            print("sending out packets")
        self.operations.append(data_packet)

    def operation_callback(self, master, packet):
        for operation in self.operations:
            if operation.operation_id == packet.data_packet['operation_reference']:
                operation.process_progress_packet(packet.data_packet)

    def main(self, master):
        pass

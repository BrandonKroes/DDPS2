import datetime
import os
import subprocess
import time

from common.communication.endpoint_config import EndpointConfig
from common.packets.blender_render_packet import BlenderRenderPacket
from common.packets.job_type import JobType
from common.packets.new_job_packet import NewJobPacket
from master.classes.cluster_config import ClusterConfiguration


class BlenderOperation:
    job_type = JobType.OPERATION
    operation_id = 0
    finished = False
    blender_file_path = ""
    start_frame = ""
    stop_frame = ""
    engine = ""
    capable_nodes = []
    packets = []
    orchestrated = False
    start_time = ""
    end_time = ""

    def __init__(self, operation_id, data_packet):
        self.operation_id = operation_id
        self.blender_file = data_packet['blender_file_path']
        self.start_frame = data_packet['start_frame']
        self.stop_frame = data_packet['stop_frame']
        self.engine = data_packet['engine']
        self.output_path = data_packet['output_path']

    def orchestrate_cluster(self, nodes):

        self.start_time = datetime.datetime.now()

        # TODO: Dynamically assign the workload i.e. a node with an iGPU should get a less work than a node with a A6000
        packet_id = 0
        frames = self.stop_frame - self.start_frame

        frames_per_node = self.get_evenly_divided_values(frames, len(nodes))
        start_iter_frames = self.start_frame

        packet_count = len(nodes)

        for i in range(len(nodes)):
            brp = BlenderRenderPacket(packet_id, job_type=JobType.RENDER,
                                      data_packet={
                                          'operation_reference': self.operation_id,
                                          'packet_reference': packet_id,
                                          'blender_file_path': self.blender_file_path,
                                          'start_frame': start_iter_frames,
                                          'stop_frame': start_iter_frames + frames_per_node[i],
                                          'output_folder': self.output_path + str(self.operation_id) + "/",
                                          'engine': self.engine
                                      })

            print(nodes[i][0])
            ec = EndpointConfig(host=nodes[i][0]['worker']['host'],
                                port=nodes[i][0]['worker']['port'],
                                packet=brp)
            self.packets.append(ec)
            start_iter_frames = start_iter_frames + frames_per_node[i]
            packet_id += 1

        self.orchestrated = True

    def node_failure(self, master, failure_node):
        # check which jobs the node had
        to_be_redistributed: EndpointConfig = None
        packets = []
        for endpoint in self.packets:
            if endpoint.host == failure_node['worker']['host'] and endpoint.port == failure_node['worker']['port']:
                to_be_redistributed = endpoint
            else:
                packets.append(endpoint)

        if to_be_redistributed is None:
            # this operation had nothing to do with this task!
            return

        # TODO: Dynamically decide which node should be picked!
        default_node = master.nodes[0]
        node_info = default_node[0]

        # Redirecting the packet to a different node!
        to_be_redistributed.host = node_info['worker']['host']
        to_be_redistributed.port = node_info['worker']['port']

        master.send_packet(to_be_redistributed)
        packets.append(to_be_redistributed)
        self.packets = packets

    @staticmethod
    def get_evenly_divided_values(value_to_be_distributed, times):
        return [value_to_be_distributed // times + int(x < value_to_be_distributed % times) for x in range(times)]

    def get_packets(self):
        t_packet = self.packets
        return t_packet

    def process_progress_packet(self, received_packet):
        backup_packet = []
        for packet in self.packets:
            print(received_packet)
            if packet.packet.data_packet['packet_reference'] != received_packet['packet_reference']:
                backup_packet.append(packet)
        self.packets = backup_packet

        if 0 == len(backup_packet):
            self.on_cluster_complete()

    def print(self):
        print(self.__dict__)

    def on_cluster_complete(self):

        render_process = subprocess
        render_process.call(["ffmpeg -nostdin -y -framerate 30 -pattern_type glob -i '" + self.output_path + '/' + str(
            self.operation_id) + "/*.png' -c:v libx264 -pix_fmt yuv420p " + str(
            self.operation_id) + ".mp4 > /dev/null 2>&1 < /dev/null "], shell=True, stdout=False)

        self.finished = True
        self.end_time = datetime.datetime.now()
        self.total_time = self.end_time - self.start_time
        print('start time: ' + self.start_time.strftime("%d/%m/%Y %H:%M:%S"))
        print('end time: ' + self.end_time.strftime("%d/%m/%Y %H:%M:%S"))
        print('duration: ' + str(self.total_time.total_seconds()))

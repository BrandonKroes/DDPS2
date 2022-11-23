import os

from common.communication.endpoint_config import EndpointConfig
from common.packets.jobs import JobType
from common.packets.new_job_packet import NewJobPacket
from master.classes.cluster_config import ClusterConfiguration

import ffmpeg


class Blender:
    operation_id = 0
    finished = False
    blender_file_path = ""
    start_frame = ""
    stop_frame = ""
    engine = ""
    capable_nodes = []
    packets = []

    def __init__(self, operation_id, output_path, blender_file_path, start_frame, stop_frame, engine):
        self.operation_id = operation_id
        self.blender_file = blender_file_path
        self.start_frame = start_frame
        self.stop_frame = stop_frame
        self.engine = engine
        self.output_path = output_path

    def orchestrate_cluster(self, cluster_config: ClusterConfiguration):
        for node in cluster_config.nodes:
            try:
                if node.blender_capable:
                    self.capable_nodes.append(node)
            except AttributeError:
                pass

        # TODO: Dynamically assign the workload i.e. a node with an iGPU should get a less work than a node with a A6000
        packet_id = 0
        frames = self.stop_frame - self.start_frame

        frames_per_node = frames / len(self.capable_nodes)

        start_iter_frames = self.start_frame
        for node in self.capable_nodes[:-1]:
            njp = NewJobPacket(packet_id, job_type=JobType.RENDER,
                               data_packet={
                                   'blender_file_path': self.blender_file_path,
                                   'start_frame': start_iter_frames,
                                   'stop_frame': start_iter_frames + frames_per_node,
                                   'output_folder': self.output_path + self.operation_id + "/",
                                   'engine': self.engine
                               })
            ec = EndpointConfig(host=node.host, port=node.port, packet=njp)
            self.packets.append(ec)
            start_iter_frames = start_iter_frames + frames_per_node
            packet_id += 1

        njp = NewJobPacket(packet_id, job_type=JobType.RENDER,
                           data_packet={
                               'blender_file_path': self.blender_file_path,
                               'start_frame': start_iter_frames,
                               'stop_frame': self.stop_frame,
                               'output_folder': self.output_path + self.operation_id + "/",
                               'engine': self.engine
                           })
        ec = EndpointConfig(host=self.capable_nodes[-1].host, port=self.capable_nodes[-1].port, packet=njp)
        self.packets.append(ec)

    def get_packets(self):
        return self.packets

    def process_progress_packet(self, packet):
        pass

    def on_cluster_complete(self):
        os.system(
            "ffmpeg -framerate 30 -pattern_type glob -i '" + self.output_path + "*.png' -c:v libx264 -pix_fmt yuv420p " + self.operation_id + ".mp4")
        self.finished = True

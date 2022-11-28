import sys
import os.path

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from common.packets.jobs import JobType
from common.packets.shutdown_packet import ShutdownPacket
from master.master_daemon import MasterDaemon

njp = ShutdownPacket(packet_id="1", job_type=JobType.RENDER,
                     data_packet={
                         'blender_file_path': '/home/brand/lu/ddps/assignment2/example/example.blend',
                         'start_frame': 1, 'stop_frame': 4,
                         'output_folder': "/home/brand/lu/ddps/assignment2/example/3/",
                         'engine': "CYCLES"})

md = MasterDaemon("../config/conf.yaml")
# md.process_packet_operation(njp)
md.main()

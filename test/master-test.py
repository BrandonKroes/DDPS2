import sys
import os.path

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
from daemons import MasterDaemon
from common.packets import ShutdownPacket, JobType

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

njp = ShutdownPacket(packet_id="1", job_type=JobType.RENDER,
                     data_packet={
                         'blender_file_path': '/home/brand/lu/ddps/assignment2/example/example.blend',
                         'start_frame': 1, 'stop_frame': 4,
                         'output_folder': "/home/brand/lu/ddps/assignment2/example/3/",
                         'engine': "CYCLES"})

md = MasterDaemon("/home/brand/lu/ddps/assignment2/config/conf.yaml")
md.boot()
# md.process_packet_operation(njp)
md.main()

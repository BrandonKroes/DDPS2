import sys
import os.path

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
from daemons import WorkerDaemon
from common.packets import BlenderRenderPacket
from common.packets.job_type import JobType

njp = BlenderRenderPacket(packet_id="1", job_type=JobType.RENDER,
                          data_packet={
                              'blender_file_path': '/home/brand/lu/ddps/assignment2/example/example.blend',
                              'start_frame': 1, 'stop_frame': 4,
                              'output_folder': "/home/brand/lu/ddps/assignment2/example/3/",
                              'engine': "CYCLES"})
wd = WorkerDaemon("../config/conf.yaml")
#wd.add_scheduled_job(njp)
#wd.execute_new_job()
wd.boot()
wd.main()

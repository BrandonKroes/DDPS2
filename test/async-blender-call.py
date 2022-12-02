import sys
import os.path

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
from common.packets import NewOperationPacket, JobType
from master.operations import BlenderOperation
from daemons import WorkerDaemon

njp = BlenderOperation(1, data_packet={
    'job_type':JobType.OPERATION,
    'blender_file_path': '/home/brand/lu/ddps/assignment2/example/example.blend',
    'start_frame': 1, 'stop_frame': 1,
    'output_path': "/home/brand/lu/ddps/assignment2/example/5/1/",
    'engine': "CYCLES"})
wd = WorkerDaemon("../config/conf.yaml")
wd.add_scheduled_job(NewOperationPacket(packet_id=1, job_type=JobType.OPERATION,
                                        data_packet=njp))
wd.main()

import sys
import os.path

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from master.operations.blender_operation import BlenderOperation


from common.packets.blender_render_packet import BlenderRenderPacket
from common.packets.new_operation_packet import NewOperationPacket

from common.packets.jobtype import JobType
from worker.worker_daemon import WorkerDaemon

njp = BlenderOperation(1, data_packet={
    'blender_file_path': '/home/brand/lu/ddps/assignment2/example/example.blend',
    'start_frame': 1, 'stop_frame': 4,
    'output_path': "/home/brand/lu/ddps/assignment2/example/4/",
    'engine': "CYCLES"})
wd = WorkerDaemon("../config/conf.yaml")
wd.add_scheduled_job(NewOperationPacket(packet_id=1, job_type=JobType.OPERATION,
                                        data_packet=njp))
wd.main()

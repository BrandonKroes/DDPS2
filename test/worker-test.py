from common.packets.jobs import JobType
from common.packets.new_job_packet import NewJobPacket
from worker.worker_daemon import WorkerDaemon

njp = NewJobPacket(packet_id="1", job_type=JobType.RENDER,
                   data_packet={
                       'blender_file_path': '/home/brand/lu/ddps/assignment2/example/example.blend',
                       'start_frame': 1, 'stop_frame': 4,
                       'output_folder': "/home/brand/lu/ddps/assignment2/example/3/",
                       'engine': "CYCLES"})
wd = WorkerDaemon()
wd.add_scheduled_job(njp)

wd.main()

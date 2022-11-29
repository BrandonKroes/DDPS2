from common.packets.abstract_packet import AbstractPacket
from worker.tasks.task_blender import TaskBlender


class BlenderRenderPacket(AbstractPacket):

    def __init__(self, packet_id, job_type, data_packet):
        super().__init__(packet_id, job_type, data_packet)

    def execute_worker_side(self, worker):
        print('started')
        self.data_packet['blender_path'] = worker.blender_path
        jb = TaskBlender(**self.data_packet)
        jb.execute()
        print('done')
        worker.actively_working = False

    def execute_master_side(self, master):
        pass

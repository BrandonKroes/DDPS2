from common.packets import AbstractPacket
from worker.tasks.task_blender import TaskBlender


class BlenderRenderPacket(AbstractPacket):

    def __init__(self, packet_id, job_type, data_packet):
        super().__init__(packet_id, job_type, data_packet)
        self.finished = False

    def execute_worker_side(self, worker):
        print('started')
        self.data_packet['blender_path'] = worker.blender_path
        try:
            self.data_packet['cycles_device'] = worker.conf['worker']['cycles_device']
        except KeyError:
            self.data_packet['cycles_device'] = "undefined"
        jb = TaskBlender(**self.data_packet)
        jb.execute(worker)
        # print('done')
        # worker.actively_working = False

    def done_worker_side(self, worker: 'WorkerDaemon'):
        from common.communication import EndpointConfig
        self.finished = True
        worker.outgoing_request.send(EndpointConfig(packet=self, port=worker.master_port, host=worker.master_host))

    def execute_master_side(self, master):
        master.operations_manager.operation_callback(data_packet=self.data_packet, master=self)

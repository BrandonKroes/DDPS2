from worker.tasks.task_abstract import AbstractTask


class TaskHeartbeat(AbstractTask):

    def __init__(self):
        pass

    def execute(self):
        pass

    def is_finished(self):
        pass

    @staticmethod
    def is_capable():
        return True

import subprocess

from worker.tasks import AbstractTask


class TaskBlender(AbstractTask):
    conf = {
        'blender_path': "unset",
        'blender_file_path': 'unset',
        'start_frame': 'unset',
        'stop_frame': 'unset',
        'engine': 'unset',
        'cycles_device': 'undefined',
        'job_id': 'undefined',
        'output_folder': 'unset',
    }
    finished = False
    running = False
    init = False
    progress = 0
    render_process = None

    def __init__(self, **kwargs):
        # read config to override at run time.
        for key, val in self.conf.items():
            self.__dict__[key] = kwargs.get(key, val)

    def is_finished(self):
        return self.finished

    def execute(self):
        if 'unset' in self.__dict__:
            # TODO: Throw exception
            return print("Unset value is supplied. blender_file_path, start_frame, stop_frame and engine are mandatory")

        extra_args = []
        if self.conf.get('engine') is "CYCLES" and self.conf.get('cycles_device') is not "undefined":
            extra_args = ["--cycles-device " + self.conf.get('cycles_device')]
        
        args = [
            ' --background',  # Setting Blender to background/headless config
            self.blender_file_path,
            '--engine', self.engine,
            '--frame-start', str(self.start_frame),
            '--frame-end', str(self.stop_frame),
            '--render-output', str(self.output_folder)
        ]
        extra_args = extra_args + [' -a']  # Render the whole animation using all the settings saved in the blend-file.

        self.running = True
        self.render_process = subprocess
        self.render_process.call([self.blender_path + " ".join(args) + " ".join(extra_args)], shell=True, stdout=False)
        self.finished = True

    def render_status(self):
        if self.init:
            return "Starting blender render."
        return "At frame %1 from the %2. Using Engine %3".format(str(self.progress), str(self.stop_frame), self.engine)

    @staticmethod
    def is_capable():
        return True

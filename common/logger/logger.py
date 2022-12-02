class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


# function to instantiate data in memory
# function to establish database
# function to establish scratch disk
class Logger(metaclass=Singleton):
    def __init__(self, conf):
        pass

    def append_record(self, record):
        pass

    def instantiate_db(self):
        pass

    def instantiate_scratch_file(self):
        pass

    def instantiate_in_memory(self):
        pass

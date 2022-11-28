from enum import Enum


class JobType(Enum):
    UNDEFINED = 0
    RENDER = 1
    STATUS = 2
    REGISTER = 3
    SHUTDOWN = 4


from abc import ABC
from enum import Enum


class OperatorTypes(Enum):
    MASTER = "master"
    WORKER = "worker"


class OperatorDaemon(ABC):

    def __init__(self, operator_type: OperatorTypes):
        self.operatorType = operator_type

# new clients
# new tasks
# status
# merging
# assigning tasks
# file management
# user input
# reschedule
# failsafe

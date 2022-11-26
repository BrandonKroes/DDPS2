from abc import ABC
from enum import Enum


class OperatorTypes(Enum):
    MASTER = "master"
    WORKER = "worker"


class Operator(ABC):

    def __init__(self, operator_type: OperatorTypes):
        self.operatorType = operator_type

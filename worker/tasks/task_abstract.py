import abc
from abc import ABC, abstractmethod


class AbstractTask(ABC):

    def execute(self):
        pass

    def is_finished(self):
        pass

    # checks if a host is actually capable of performing this task.
    @staticmethod
    def is_capable():
        pass

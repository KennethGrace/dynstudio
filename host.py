
from abc import ABC, abstractmethod

class Host(ABC):
    name = 'null'

    def __init__(self, name):
        self.name = name
        pass

    @abstractmethod
    def connect(self):
        print("Log from Host")
        pass
# level.py
import abc
from ursina import *

class Level(abc.ABC):
    def __init__(self, name, difficulty):
        self.name = name
        self.difficulty = difficulty

    @abc.abstractmethod
    def setup_level(self):
        pass

    @abc.abstractmethod
    def start(self):
        pass

    @abc.abstractmethod
    def complete(self):
        pass



# class Level1(Level):
#     pass
# class Level2(Level):
#     pass
# class Level3(Level):
#     pass


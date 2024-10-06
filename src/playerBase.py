
from abc import ABC, abstractmethod

from actions import ActionBase
from state import State


class PlayerBase(ABC):
    def __init__(self, name: str):
        self.name: str = name

    @abstractmethod
    def act(self, state: State, actions: list[ActionBase]) -> ActionBase:
        pass

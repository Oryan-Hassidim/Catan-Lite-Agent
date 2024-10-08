
from abc import ABC, abstractmethod
from typing import Iterable

from actions import ActionBase
from state import GameState


class PlayerBase(ABC):
    def __init__(self, name: str):
        self.name: str = name

    @abstractmethod
    def choose_action(self, state: GameState, actions: Iterable[ActionBase]) -> ActionBase:
        raise NotImplementedError()

    @abstractmethod
    def reward(self, reward: float):
        raise NotImplementedError()

class RandomPlayer(PlayerBase):
    def choose_action(self, state: GameState, actions: Iterable[ActionBase]) -> ActionBase:
        import random
        return random.choice(list(actions))

    def reward(self, reward: float):
        pass

class HumanPlayer(PlayerBase):
    def choose_action(self, state: GameState, actions: Iterable[ActionBase]) -> ActionBase:
        print("Choose an action:")
        actions = list(actions)
        for i, action in enumerate(actions):
            print(f"{i:<2}: {action}")
        choice = int(input())
        return actions[choice]

    def reward(self, reward: float):
        pass
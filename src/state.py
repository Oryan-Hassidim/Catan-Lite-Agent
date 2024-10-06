
from dataclasses import dataclass

from dupfrozenset import dupfrozenset
from enums import BuildingType, RessourceType, HOME, CITY, WOOD, STONE, GOLD, FOOD
from frozenCounter import frozenCounter


@dataclass(frozen=True)
class PlayerState:
    Buildings: frozenCounter[BuildingType]
    Resources: int


@dataclass(frozen=True)
class State:
    YourBuildings: frozenCounter[BuildingType]
    YourResources: frozenCounter[RessourceType]
    OtherPlayers: dupfrozenset[PlayerState]


if __name__ == "__main__":
    state: State = State(frozenCounter({HOME: 1, CITY: 2}),
                         frozenCounter(
                             {WOOD: 10, STONE: 20, GOLD: 30, FOOD: 40}),
                         dupfrozenset([PlayerState(frozenCounter({HOME: 1, CITY: 2}), 100)]))

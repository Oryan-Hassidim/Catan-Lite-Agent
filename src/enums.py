
from enum import StrEnum

from frozenCounter import frozenCounter


class RessourceType(StrEnum):
    WOOD = "wood"
    STONE = "stone"
    GOLD = "gold"
    FOOD = "food"


WOOD = RessourceType.WOOD
STONE = RessourceType.STONE
GOLD = RessourceType.GOLD
FOOD = RessourceType.FOOD


class BuildingType(StrEnum):
    HOME = "home"
    CITY = "city"

    def get_cost(self) -> frozenCounter['RessourceType']:
        if self == HOME:
            return frozenCounter({WOOD: 1, STONE: 1})
        if self == CITY:
            return frozenCounter({WOOD: 2, STONE: 2})
        raise ValueError(f"Unknown building type {self}")


HOME = BuildingType.HOME
CITY = BuildingType.CITY

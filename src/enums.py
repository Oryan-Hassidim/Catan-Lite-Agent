
from enum import StrEnum

from frozenCounter import frozenCounter


class RessourceType(StrEnum):
    WOOD = "wood"
    STONE = "stone"


WOOD = RessourceType.WOOD
STONE = RessourceType.STONE


class BuildingType(StrEnum):
    HOUSE = "house"
    CITY = "city"

    def get_cost(self) -> frozenCounter['RessourceType']:
        if self == HOUSE:
            return frozenCounter({WOOD: 2, STONE: 1})
        if self == CITY:
            return frozenCounter({WOOD: 2, STONE: 2})
        raise ValueError(f"Unknown building type {self}")
    
    def get_score(self) -> int:
        if self == HOUSE:
            return 1
        if self == CITY:
            return 2
        raise ValueError(f"Unknown building type {self}")


HOUSE = BuildingType.HOUSE
CITY = BuildingType.CITY


from abc import ABC
from enums import BuildingType, RessourceType
from frozenCounter import frozenCounter


class ActionBase(ABC):
    def __init__(self, name: str):
        self._name: str = name

    @property
    def name(self) -> str:
        return self._name

    def __str__(self) -> str:
        return self._name

    def __repr__(self) -> str:
        return self._name

    def __eq__(self, other: 'ActionBase') -> bool:
        return self._name == other._name

    def __hash__(self) -> int:
        return hash(self._name)


class BuildAction(ActionBase):
    def __init__(self, type: BuildingType):
        super().__init__(f"Build {type}")
        self._type = type

    @property
    def type(self) -> BuildingType:
        return self._type


class OfferADealAction(ActionBase):
    def __init__(self, playerIndex: int, give: frozenCounter[RessourceType], take: frozenCounter[RessourceType]):
        super().__init__(
            f"Offer a deal to player {playerIndex}: give {give}, take {take}")
        self._playerIndex = playerIndex
        self._give = give
        self._take = take

    @property
    def playerIndex(self) -> int:
        return self._playerIndex

    @property
    def give(self) -> frozenCounter[RessourceType]:
        return self._give

    @property
    def take(self) -> frozenCounter[RessourceType]:
        return self._take


class AnswerADealAction(ActionBase):
    def __init__(self, playerIndex: int, give: frozenCounter[RessourceType],
                 take: frozenCounter[RessourceType], accepted: bool):
        super().__init__(f"Answer a deal from player {playerIndex}: "
                         f"give {give}, take {take}, accepted: {accepted}")
        self._playerIndex = playerIndex
        self._give = give
        self._take = take
        self._accepted = accepted

    @property
    def playerIndex(self) -> int:
        return self._playerIndex

    @property
    def give(self) -> frozenCounter[RessourceType]:
        return self._give

    @property
    def take(self) -> frozenCounter[RessourceType]:
        return self._take

    @property
    def accepted(self) -> bool:
        return self._accepted


class NoOpAction(ActionBase):
    def __init__(self):
        super().__init__("NoOp")


from collections import Counter
from dataclasses import dataclass
from itertools import chain

from frozenlist import frozenlist
from enums import BuildingType, RessourceType
from frozenCounter import frozenCounter
from playerBase import PlayerBase
from parameters import PARAMETERS


@dataclass(frozen=True)
class PlayerState:
    _index: int
    _buildings: frozenCounter[BuildingType]
    _resources: frozenCounter[RessourceType]

    @property
    def index(self) -> int:
        return self._index

    @property
    def buildings(self) -> frozenCounter[BuildingType]:
        return self._buildings

    @property
    def resources(self) -> frozenCounter[RessourceType]:
        return self._resources

    @property
    def score(self) -> int:
        return sum(count * building.get_score()
                   for building, count in self._buildings.items())


@dataclass
class Deal:
    _player_shift: int
    _resources_offered: frozenCounter[RessourceType]
    _resources_requested: frozenCounter[RessourceType]

    @property
    def player_shift(self) -> int:
        return self._player_shift

    @property
    def resources_offered(self) -> frozenCounter[RessourceType]:
        return self._resources_offered

    @property
    def resources_requested(self) -> frozenCounter[RessourceType]:
        return self._resources_requested


@dataclass(frozen=True)
class GameState:
    _players: frozenlist[PlayerState]
    _offer: None | Deal

    @property
    def players(self) -> frozenlist[PlayerState]:
        return self._players

    @property
    def offer(self) -> None | Deal:
        return self._offer

    @property
    def current_player(self) -> PlayerState:
        return self._players[0]

    @property
    def game_over(self) -> bool:
        return any(player.score >= PARAMETERS.WIN_SCORE
                   for player in self._players)

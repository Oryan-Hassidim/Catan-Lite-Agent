
from abc import ABC, abstractmethod
from typing import Generator
from frozenlist import frozenlist
from parameters import PARAMETERS
from enums import BuildingType, RessourceType
from frozenCounter import frozenCounter
from state import GameState, Deal, PlayerState


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

    @abstractmethod
    def act(self, state: GameState) -> GameState:
        raise NotImplementedError()


class BuildAction(ActionBase):
    def __init__(self, type: BuildingType):
        super().__init__(f"Build {type}")
        self._type = type

    @property
    def type(self) -> BuildingType:
        return self._type

    def act(self, state: GameState) -> GameState:
        player: PlayerState = state.players[0]
        building: frozenCounter[BuildingType] = frozenCounter({self._type: 1})
        cost = self._type.get_cost()
        if cost not in player.resources:
            raise ValueError(
                f"Player {player} does not have enough resources to build {self._type}")
        playerState = PlayerState(player._index,
                                  player._buildings + building,
                                  player.resources - cost)
        players = state.players.update_item(0, playerState).rotate()
        return GameState(players, None)

    @staticmethod
    def get_all_actions(state: GameState) -> Generator[ActionBase]:
        if state.offer is not None:
            return
        player = state.players[0]
        for building in BuildingType:
            if building.get_cost() in player.resources:
                yield BuildAction(building)


class OfferADealAction(ActionBase):
    def __init__(self, deal: Deal):
        super().__init__(
            f"Offer a deal {deal}")
        self._deal: Deal = deal

    @property
    def deal(self) -> Deal:
        return self._deal

    def act(self, state: GameState) -> GameState:
        return GameState(state.players.rotate(self._deal.player_shift),
                         self._deal)

    @staticmethod
    def get_all_actions(state: GameState) -> Generator[ActionBase]:
        if state.offer is not None:
            return
        player = state.players[0]
        for player_shift in range(1, len(state.players)):
            other_player = state.players[player_shift]
            for resource_offered in player.resources:
                for resource_requested in other_player.resources:
                    if resource_offered == resource_requested:
                        continue
                    for amount_offered in range(1, player.resources[resource_offered]):
                        for amount_requested in range(1, other_player.resources[resource_requested]):
                            deal = Deal(player_shift,
                                        frozenCounter(
                                            {resource_offered: amount_offered}),
                                        frozenCounter({resource_requested: amount_requested}))
                            yield OfferADealAction(deal)


class AnswerADealAction(ActionBase):
    def __init__(self, accept: bool):
        super().__init__(f"Answer a deal {accept}")
        self._accept: bool = accept

    @property
    def accept(self) -> bool:
        return self._accept

    def act(self, state: GameState) -> GameState:
        if state.offer is None:
            raise ValueError("There is no deal to answer")
        if self._accept:
            player: PlayerState = state.players[0]
            playerState = PlayerState(player._index,
                                      player._buildings,
                                      player.resources + state.offer.resources_offered - state.offer.resources_requested)
            players: frozenlist[PlayerState] = state.players.update_item(
                0, playerState).rotate(-state.offer.player_shift)
            player: PlayerState = players[0]
            playerState = PlayerState(player._index,
                                      player._buildings,
                                      player.resources
                                      + state.offer.resources_requested
                                      - state.offer.resources_offered)
            players = players.update_item(0, playerState)
            return GameState(players, None)
        else:
            return GameState(state.players.rotate(-state.offer.player_shift),
                             None)

    @staticmethod
    def get_all_actions(state: GameState) -> Generator[ActionBase]:
        if state.offer is not None:
            yield AnswerADealAction(True)
            yield AnswerADealAction(False)


class BuyAction(ActionBase):
    def __init__(self, ressource_requested: RessourceType, resource_offered: RessourceType):
        super().__init__(f"Buy {ressource_requested} with {resource_offered}")
        self._ressource_requested: RessourceType = ressource_requested
        self._resource_offered: RessourceType = resource_offered

    @property
    def ressource_requested(self) -> RessourceType:
        return self._ressource_requested

    @property
    def resource_offered(self) -> RessourceType:
        return self._resource_offered

    def act(self, state: GameState) -> GameState:
        player: PlayerState = state.players[0]
        if player.resources[self._resource_offered] < PARAMETERS.BANK_COST:
            raise ValueError(
                f"Player {player} does not have enough {self._resource_offered} to buy {self._ressource_requested}")
        playerState = PlayerState(player._index,
                                  player._buildings,
                                  player.resources
                                  + frozenCounter({self._ressource_requested: 1})
                                  - frozenCounter({self._resource_offered: PARAMETERS.BANK_COST}))
        players = state.players.update_item(0, playerState)
        return GameState(players, None)

    @staticmethod
    def get_all_actions(state: GameState) -> Generator[ActionBase]:
        if state.offer is not None:
            return
        player = state.players[0]
        for resource_offered in player.resources:
            for resource_requested in RessourceType:
                if resource_offered == resource_requested:
                    continue
                if player.resources[resource_offered] < PARAMETERS.BANK_COST:
                    continue
                yield BuyAction(resource_requested, resource_offered)


class PassAction(ActionBase):
    def __init__(self):
        super().__init__("NoOp")

    def act(self, state: GameState) -> GameState:
        return GameState(state.players.rotate(), None)

    @staticmethod
    def get_all_actions(state: GameState) -> Generator[ActionBase]:
        if state.offer is not None:
            return
        yield PassAction()

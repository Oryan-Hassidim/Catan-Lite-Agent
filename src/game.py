
from collections import Counter
from dataclasses import dataclass

from actions import ActionBase, BuildAction, OfferADealAction, AnswerADealAction, NoOpAction
from dupfrozenset import dupfrozenset
from enums import BuildingType, RessourceType
from frozenCounter import frozenCounter
from playerBase import PlayerBase
from state import PlayerState, State


class Game:

    @dataclass
    class Player:
        Player: PlayerBase
        Buildings: Counter[BuildingType]
        Resources: Counter[RessourceType]

    @dataclass
    class Offer:
        fromPlayerIndex: int
        toPlayerIndex: int
        resources_offered: frozenCounter[RessourceType]
        resources_requested: frozenCounter[RessourceType]

    def __init__(self, players: list[PlayerBase]) -> None:
        self._state: list[Game.Player] = [Game.Player(player, Counter(), Counter())
                                          for player in players]
        self._offer: None | Game.Offer = None

    def _generate_state(self, playerIndex: int) -> State:
        player = self._state[playerIndex]
        return State(frozenCounter(player.Buildings),
                     frozenCounter(player.Resources),
                     dupfrozenset([PlayerState(frozenCounter(player.Buildings),
                                               player.Resources.total())
                                   for i, player in enumerate(self._state)
                                   if i != playerIndex]))

    def _generate_actions(self, playerIndex: int) -> list[ActionBase]:
        state: State = self._generate_state(playerIndex)
        if self._offer is not None:
            return [AnswerADealAction(self._offer.fromPlayerIndex,
                                      self._offer.resources_offered,
                                      self._offer.resources_requested,
                                      accepted)
                    for accepted in (True, False)]
        actions = []
        for type in BuildingType:
            if type.get_cost() in state.YourResources:
                actions.append(BuildAction(type))

        for i, player in enumerate(self._state):
            if i == playerIndex:
                continue

        return actions

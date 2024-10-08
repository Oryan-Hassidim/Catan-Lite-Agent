
import datetime
from typing import Generator
from actions import ActionBase
from frozenlist import frozenlist
from frozenCounter import frozenCounter
from playerBase import PlayerBase
from state import GameState, PlayerState

import logging
logger = logging.getLogger(__name__)


class Game:
    def __init__(self, players: list[PlayerBase]):
        self._players = list(players)
        self._state: GameState = GameState(
            frozenlist(
                *(PlayerState(i, frozenCounter(), frozenCounter())
                  for i, _ in enumerate(players))),
            None)
        logger.info("Game initialized with players %s", players)

    @property
    def state(self) -> GameState:
        return self._state

    @state.setter
    def state(self, value: GameState):
        logger.info("Setting state from %s to %s", self._state, value)
        self._state = value

    @staticmethod
    def _generate_actions(state: GameState) -> Generator[ActionBase]:
        from actions import BuildAction, OfferADealAction, AnswerADealAction, BuyAction, PassAction
        yield from BuildAction.get_all_actions(state)
        yield from OfferADealAction.get_all_actions(state)
        yield from AnswerADealAction.get_all_actions(state)
        yield from BuyAction.get_all_actions(state)
        yield from PassAction.get_all_actions(state)

    def _play_turn(self):
        player: PlayerBase = self._players[0]
        actions = self._generate_actions(self.state)
        action = player.choose_action(self.state, actions)
        logger.info("Player %s chose action %s", player, action)
        self.state = action.act(self.state)
        player.reward(0)

    def play(self):
        logger.info("Starting game at time %s", datetime.datetime.now())
        while not self.state.game_over:
            self._play_turn()
        logger.info("Game ended at time %s", datetime.datetime.now())

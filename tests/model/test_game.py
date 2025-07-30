import pytest
from model.dealer_hand import DealerHand
from exceptions.hand_exceptions import InitialDrawError
from enums.decisions import DealerDecision
from game_logic.game import Game
from utils.logger import logger
def test_16_v_10():
    game = Game(player_bankroll=10000)
    game.shoe.shoe.extend([6,10,10])
    game.deal_initial_cards()
    assert len(game.hands_to_play) == 1
    assert game.hands_to_play[0].get_value() == 16
    assert game.dealer_hand.get_upcard() == 10

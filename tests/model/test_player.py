import pytest
from model.player import Player
from exceptions.player_exceptions import NegativeBankrollError

def test_player_initialization():
    pass

def test_negative_bankroll_initialization():

    with pytest.raises(NegativeBankrollError) as excinfo:
        player = Player(bankroll = -1)

    assert "Player bankroll is negative" in str(excinfo.value)


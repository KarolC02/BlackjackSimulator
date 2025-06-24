import pytest
from model.dealer_hand import DealerHand
from exceptions.hand_exceptions import InitialDrawError
from enums.decisions import DealerDecision

def test_2():
    hand = DealerHand()
    hand.draw(2)
    assert hand.select_dealer_move() == DealerDecision.HIT

def test_7():
    hand = DealerHand()
    hand.draw(7)
    assert hand.select_dealer_move() == DealerDecision.HIT

def test_10():
    hand = DealerHand()
    hand.draw(10)
    assert hand.select_dealer_move() == DealerDecision.HIT

def test_11():
    hand = DealerHand()
    hand.draw(11)
    assert hand.select_dealer_move() == DealerDecision.HIT

def test_8_8():
    hand = DealerHand()
    hand.draw(8)
    hand.draw(8)
    assert hand.select_dealer_move() == DealerDecision.HIT

def test_10_6():
    hand = DealerHand()
    hand.draw(10)
    hand.draw(6)
    assert hand.select_dealer_move() == DealerDecision.HIT

def test_two_card_17():
    hand = DealerHand()
    hand.draw(10)
    hand.draw(7)
    assert hand.select_dealer_move() == DealerDecision.STAND

def test_three_card_17():
    hand = DealerHand()
    hand.draw(10)
    hand.draw(5)
    hand.draw(2)
    assert hand.select_dealer_move() == DealerDecision.STAND

def test_two_card_soft_17():
    hand = DealerHand()
    hand.draw(11)
    hand.draw(6)
    assert hand.select_dealer_move() == DealerDecision.STAND

def test_two_card_soft_17_h17():
    hand = DealerHand(s17=False)
    hand.draw(11)
    hand.draw(6)
    assert hand.select_dealer_move() == DealerDecision.HIT


def test_three_card_soft_17():
    hand = DealerHand()
    hand.draw(11)
    assert hand.select_dealer_move() == DealerDecision.HIT
    hand.draw(3)
    assert hand.select_dealer_move() == DealerDecision.HIT
    hand.draw(3)
    assert hand.select_dealer_move() == DealerDecision.STAND

def test_three_card_soft_17_h17():
    hand = DealerHand(s17 = False)
    hand.draw(11)
    assert hand.select_dealer_move() == DealerDecision.HIT
    hand.draw(3)
    assert hand.select_dealer_move() == DealerDecision.HIT
    hand.draw(3)
    assert hand.select_dealer_move() == DealerDecision.HIT


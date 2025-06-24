import pytest
from model.player_hand import PlayerHand
from model.dealer_hand import DealerHand
from enums.decisions import PlayerDecision, DealerDecision
from strategy.basic_strategy import BasicStrategy

strategy_book = BasicStrategy()

#############################################################
######################### Surrender #########################
#############################################################

def test_10_6_vs_10_surrender():
    hand = PlayerHand()
    hand.initial_draw(10)
    hand.initial_draw(6)
    dealer_up_card = 10
    assert strategy_book.pick_action(hand,dealer_up_card) == PlayerDecision.SURRENDER

def test_10_4_2_vs_10_hit():
    hand = PlayerHand()
    hand.initial_draw(10)
    hand.initial_draw(4)
    hand.draw(2)
    dealer_up_card = 10
    assert strategy_book.pick_action(hand,dealer_up_card) == PlayerDecision.HIT

def test_10_6_vs_9_surrender():
    hand = PlayerHand()
    hand.initial_draw(10)
    hand.initial_draw(6)
    dealer_up_card = 9
    assert strategy_book.pick_action(hand,dealer_up_card) == PlayerDecision.SURRENDER

def test_10_3_3_vs_9_hit():
    hand = PlayerHand()
    hand.initial_draw(10)
    hand.initial_draw(3)
    hand.draw(3)
    dealer_up_card = 9
    assert strategy_book.pick_action(hand,dealer_up_card) == PlayerDecision.HIT

def test_10_5_vs_10_surrender():
    hand = PlayerHand()
    hand.initial_draw(10)
    hand.initial_draw(5)
    dealer_up_card = 10
    assert strategy_book.pick_action(hand,dealer_up_card) == PlayerDecision.SURRENDER

def test_10_4_1_vs_10_hit():
    hand = PlayerHand()
    hand.initial_draw(10)
    hand.initial_draw(4)
    hand.draw(1)
    dealer_up_card = 10
    assert strategy_book.pick_action(hand,dealer_up_card) == PlayerDecision.HIT

def test_10_4_vs_10_surrender():
    hand = PlayerHand()
    hand.initial_draw(10)
    hand.initial_draw(4)
    dealer_up_card = 10
    assert strategy_book.pick_action(hand,dealer_up_card) == PlayerDecision.SURRENDER

def test_8_8_vs_10_surrender():
    hand = PlayerHand()
    hand.initial_draw(8)
    hand.initial_draw(8)
    dealer_up_card = 10
    assert strategy_book.pick_action(hand,dealer_up_card) == PlayerDecision.SURRENDER

def test_7_7_vs_10_surrender():
    hand = PlayerHand()
    hand.initial_draw(7)
    hand.initial_draw(7)
    dealer_up_card = 10
    assert strategy_book.pick_action(hand,dealer_up_card) == PlayerDecision.SURRENDER

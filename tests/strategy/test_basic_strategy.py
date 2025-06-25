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
    assert strategy_book.pick_action(hand,dealer_up_card, surrender_available = False) == PlayerDecision.HIT

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
    assert strategy_book.pick_action(hand,dealer_up_card, surrender_available = False) == PlayerDecision.HIT

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
    assert strategy_book.pick_action(hand,dealer_up_card, surrender_available = False) == PlayerDecision.HIT

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

#############################################################
#########################   Splits  #########################
#############################################################

def test_7_7_vs_7_split():
    hand = PlayerHand()
    hand.initial_draw(7)
    hand.initial_draw(7)
    dealer_up_card = 7
    assert strategy_book.pick_action(hand,dealer_up_card) == PlayerDecision.SPLIT

def test_7_7_vs_7_split_disabled():
    hand = PlayerHand()
    hand.initial_draw(7)
    hand.initial_draw(7)
    hand.disable_split()
    dealer_up_card = 7
    assert strategy_book.pick_action(hand,dealer_up_card) == PlayerDecision.HIT

def test_8_8_vs_9_split():
    hand = PlayerHand()
    hand.initial_draw(8)
    hand.initial_draw(8)
    dealer_up_card = 9
    assert strategy_book.pick_action(hand,dealer_up_card) == PlayerDecision.SPLIT

def test_2_2_vs_7_split():
    hand = PlayerHand()
    hand.initial_draw(2)
    hand.initial_draw(2)
    dealer_up_card = 7
    assert strategy_book.pick_action(hand,dealer_up_card) == PlayerDecision.SPLIT

def test_2_2_vs_8_no_split():
    hand = PlayerHand()
    hand.initial_draw(2)
    hand.initial_draw(2)
    hand.disable_split
    dealer_up_card = 8
    assert strategy_book.pick_action(hand,dealer_up_card) == PlayerDecision.HIT


def test_4_4_vs_5_split():
    hand = PlayerHand()
    hand.initial_draw(4)
    hand.initial_draw(4)
    dealer_up_card = 5
    assert strategy_book.pick_action(hand,dealer_up_card) == PlayerDecision.SPLIT


def test_4_4_vs_6_split():
    hand = PlayerHand()
    hand.initial_draw(4)
    hand.initial_draw(4)
    dealer_up_card = 6
    assert strategy_book.pick_action(hand,dealer_up_card) == PlayerDecision.SPLIT

def test_4_4_vs_4_no_split():
    hand = PlayerHand()
    hand.initial_draw(4)
    hand.initial_draw(4)
    dealer_up_card = 4
    assert strategy_book.pick_action(hand,dealer_up_card) == PlayerDecision.HIT

def test_4_4_vs_7_no_split():
    hand = PlayerHand()
    hand.initial_draw(4)
    hand.initial_draw(4)
    dealer_up_card = 7
    assert strategy_book.pick_action(hand,dealer_up_card) == PlayerDecision.HIT

def test_ace_ace_vs_2_to_10_split():
    hand = PlayerHand()
    hand.initial_draw(11)
    hand.initial_draw(11)


    for dealer_up_card in range(2,11):
        assert strategy_book.pick_action(hand,dealer_up_card) == PlayerDecision.SPLIT


def test_ace_ace_vs_ace_no_split():
    hand = PlayerHand()
    hand.initial_draw(11)
    hand.initial_draw(11)
    dealer_up_card = 11

    assert strategy_book.pick_action(hand,dealer_up_card) == PlayerDecision.HIT

def test_9_9_vs_2_10_no_7_split():
    hand = PlayerHand()
    hand.initial_draw(9)
    hand.initial_draw(9)
    for dealer_up_card in range(2,10):
        if dealer_up_card == 7:
            assert strategy_book.pick_action(hand,dealer_up_card) == PlayerDecision.STAND
        else:
            assert strategy_book.pick_action(hand,dealer_up_card) == PlayerDecision.SPLIT


#############################################################
#######################  Soft Hands  ########################
#############################################################

def test_soft_13():
    hand = PlayerHand()
    hand.initial_draw(11)
    hand.initial_draw(2)

    for dealer_up_card in range(2,12):
        if dealer_up_card in {5,6}:
            assert strategy_book.pick_action(hand,dealer_up_card) == PlayerDecision.DOUBLE
        else:
            assert strategy_book.pick_action(hand,dealer_up_card) == PlayerDecision.HIT

def test_soft_13_double_disabled():
    hand = PlayerHand()
    hand.initial_draw(11)
    hand.initial_draw(2)
    hand.disable_double()
    for dealer_up_card in range(2,12):
        assert strategy_book.pick_action(hand,dealer_up_card) == PlayerDecision.HIT

def test_soft_14_double():
    hand = PlayerHand()
    hand.initial_draw(11)
    hand.initial_draw(3)

    for dealer_up_card in range(2,12):
        if dealer_up_card in {5,6}:
            assert strategy_book.pick_action(hand,dealer_up_card) == PlayerDecision.DOUBLE
        else:
            assert strategy_book.pick_action(hand,dealer_up_card) == PlayerDecision.HIT

def test_soft_14_double_disabled():
    hand = PlayerHand()
    hand.initial_draw(11)
    hand.initial_draw(2)
    hand.draw(2)

    for dealer_up_card in range(2,12):
        assert strategy_book.pick_action(hand,dealer_up_card) == PlayerDecision.HIT

def test_soft_15():
    hand = PlayerHand()
    hand.initial_draw(11)
    hand.initial_draw(4)

    for dealer_up_card in range(2,12):
        if dealer_up_card in {4,5,6}:
            assert strategy_book.pick_action(hand,dealer_up_card) == PlayerDecision.DOUBLE
        else:
            assert strategy_book.pick_action(hand,dealer_up_card) == PlayerDecision.HIT

def test_soft_15_double_disabled():
    hand = PlayerHand()
    hand.initial_draw(11)
    hand.initial_draw(2)
    hand.draw(4)
    for dealer_up_card in range(2,12):
        assert strategy_book.pick_action(hand,dealer_up_card) == PlayerDecision.HIT

def test_soft_16():
    hand = PlayerHand()
    hand.initial_draw(11)
    hand.initial_draw(5)

    for dealer_up_card in range(2,12):
        if dealer_up_card in {4,5,6}:
            assert strategy_book.pick_action(hand,dealer_up_card) == PlayerDecision.DOUBLE
        else:
            assert strategy_book.pick_action(hand,dealer_up_card) == PlayerDecision.HIT

def test_soft_16_double_disabled():
    hand = PlayerHand()
    hand.initial_draw(11)
    hand.initial_draw(2)
    hand.draw(4)
    for dealer_up_card in range(2,12):
        assert strategy_book.pick_action(hand,dealer_up_card) == PlayerDecision.HIT

def test_soft_17():
    hand = PlayerHand()
    hand.initial_draw(6)
    hand.initial_draw(11)

    for dealer_up_card in range(2,12):
        if dealer_up_card in {3,4,5,6}:
            assert strategy_book.pick_action(hand,dealer_up_card) == PlayerDecision.DOUBLE
        else:
            assert strategy_book.pick_action(hand,dealer_up_card) == PlayerDecision.HIT

def test_soft_17_double_disabled():
    hand = PlayerHand()
    hand.initial_draw(11)
    hand.initial_draw(3)
    hand.draw(3)
    for dealer_up_card in range(2,12):
        assert strategy_book.pick_action(hand,dealer_up_card) == PlayerDecision.HIT

def test_soft_17_double_disabled_2():
    hand = PlayerHand()
    hand.initial_draw(11)
    hand.initial_draw(11)
    hand.draw(5)
    for dealer_up_card in range(2,12):
        assert strategy_book.pick_action(hand,dealer_up_card) == PlayerDecision.HIT

def test_soft_18():
    hand = PlayerHand()
    hand.initial_draw(7)
    hand.initial_draw(11)

    for dealer_up_card in range(2,12):
        if dealer_up_card in {3,4,5,6}:
            assert strategy_book.pick_action(hand,dealer_up_card) == PlayerDecision.DOUBLE
        elif dealer_up_card in {2,7}:
            assert strategy_book.pick_action(hand,dealer_up_card) == PlayerDecision.STAND
        else:
            assert strategy_book.pick_action(hand,dealer_up_card) == PlayerDecision.HIT



def test_soft_19():
    hand = PlayerHand()
    hand.initial_draw(8)
    hand.initial_draw(11)

    for dealer_up_card in range(2,12):
        assert strategy_book.pick_action(hand,dealer_up_card) == PlayerDecision.STAND

def test_soft_20():
    hand = PlayerHand()
    hand.initial_draw(9)
    hand.initial_draw(11)

    for dealer_up_card in range(2,12):
        assert strategy_book.pick_action(hand,dealer_up_card) == PlayerDecision.STAND

#############################################################
####################### Hard Doubles ########################
#############################################################

def test_11_double():
    hand = PlayerHand()
    hand.initial_draw(6)
    hand.initial_draw(5)

    for dealer_up_card in range(2,12):
        if dealer_up_card not in {10,11}:
            assert strategy_book.pick_action(hand,dealer_up_card) == PlayerDecision.DOUBLE
        else:
            assert strategy_book.pick_action(hand,dealer_up_card) == PlayerDecision.HIT

def test_11_double_disabled():
    hand = PlayerHand()
    hand.initial_draw(8)
    hand.initial_draw(3)
    hand.disable_double()

    for dealer_up_card in range(2,12):
        assert strategy_book.pick_action(hand,dealer_up_card) == PlayerDecision.HIT


def test_10_not_pair_double():
    hand = PlayerHand()
    hand.initial_draw(7)
    hand.initial_draw(3)

    for dealer_up_card in range(2,12):
        if dealer_up_card not in {10,11}:
            assert strategy_book.pick_action(hand,dealer_up_card) == PlayerDecision.DOUBLE
        else:
            assert strategy_book.pick_action(hand,dealer_up_card) == PlayerDecision.HIT

def test_10_not_pair_double_disabled():
    hand = PlayerHand()
    hand.initial_draw(8)
    hand.initial_draw(2)
    hand.disable_double()

    for dealer_up_card in range(2,12):
        assert strategy_book.pick_action(hand,dealer_up_card) == PlayerDecision.HIT

def test_10_pair_double():
    hand = PlayerHand()
    hand.initial_draw(5)
    hand.initial_draw(5)

    for dealer_up_card in range(2,12):
        if dealer_up_card not in {10,11}:
            assert strategy_book.pick_action(hand,dealer_up_card) == PlayerDecision.DOUBLE
        else:
            assert strategy_book.pick_action(hand,dealer_up_card) == PlayerDecision.HIT

def test_10_pair_double_disabled():
    hand = PlayerHand()
    hand.initial_draw(5)
    hand.initial_draw(5)
    hand.disable_double()

    for dealer_up_card in range(2,12):
        assert strategy_book.pick_action(hand,dealer_up_card) == PlayerDecision.HIT

def test_9_double():
    hand = PlayerHand()
    hand.initial_draw(5)
    hand.initial_draw(4)

    for dealer_up_card in range(2,12):
        if dealer_up_card in {3,4,5,6}:
            assert strategy_book.pick_action(hand,dealer_up_card) == PlayerDecision.DOUBLE
        else:
            assert strategy_book.pick_action(hand,dealer_up_card) == PlayerDecision.HIT

def test_9_double_disabled():
    hand = PlayerHand()
    hand.initial_draw(5)
    hand.initial_draw(4)
    hand.disable_double()

    for dealer_up_card in range(2,12):
        assert strategy_book.pick_action(hand,dealer_up_card) == PlayerDecision.HIT



#############################################################
####################### Hard HIT/STAND ######################
#############################################################
def test_hard_12():
    hand = PlayerHand()
    hand.initial_draw(8)
    hand.initial_draw(4)
    hand.disable_double()

    for dealer_up_card in range(2,12):
        if dealer_up_card in {4,5,6}:
            assert strategy_book.pick_action(hand,dealer_up_card) == PlayerDecision.STAND
        else:
            assert strategy_book.pick_action(hand,dealer_up_card) == PlayerDecision.HIT

def test_hard_13():
    hand = PlayerHand()
    hand.initial_draw(7)
    hand.initial_draw(6)
    hand.disable_double()

    for dealer_up_card in range(2,12):
        if dealer_up_card in {2,3,4,5,6}:
            assert strategy_book.pick_action(hand,dealer_up_card) == PlayerDecision.STAND
        else:
            assert strategy_book.pick_action(hand,dealer_up_card) == PlayerDecision.HIT

def test_hard_14_surrender_disabled():
    hand = PlayerHand()
    hand.initial_draw(7)
    hand.initial_draw(6)
    hand.draw(11)

    assert hand.get_value() == 14
    for dealer_up_card in range(2,12):
        if dealer_up_card in {2,3,4,5,6}:
            assert strategy_book.pick_action(hand,dealer_up_card, surrender_available = False) == PlayerDecision.STAND
        else:
            assert strategy_book.pick_action(hand,dealer_up_card, surrender_available = False) == PlayerDecision.HIT

def test_hard_15_surrender_disabled():
    hand = PlayerHand()
    hand.initial_draw(7)
    hand.initial_draw(6)
    hand.draw(2)

    assert hand.get_value() == 15
    for dealer_up_card in range(2,12):
        if dealer_up_card in {2,3,4,5,6}:
            assert strategy_book.pick_action(hand,dealer_up_card,  surrender_available = False) == PlayerDecision.STAND
        else:
            assert strategy_book.pick_action(hand,dealer_up_card, surrender_available = False) == PlayerDecision.HIT

def test_hard_16_surrender_disabled():
    hand = PlayerHand()
    hand.initial_draw(8)
    hand.initial_draw(6)
    hand.draw(2)

    assert hand.get_value() == 16
    for dealer_up_card in range(2,12):
        if dealer_up_card in {2,3,4,5,6}:
            assert strategy_book.pick_action(hand,dealer_up_card, surrender_available = False) == PlayerDecision.STAND
        else:
            assert strategy_book.pick_action(hand,dealer_up_card, surrender_available = False) == PlayerDecision.HIT

def test_hard_17():
    hand = PlayerHand()
    hand.initial_draw(8)
    hand.initial_draw(7)
    hand.draw(2)

    assert hand.get_value() == 17
    for dealer_up_card in range(2,12):
        assert strategy_book.pick_action(hand,dealer_up_card, surrender_available = False) == PlayerDecision.STAND

def test_hard_18():
    hand = PlayerHand()
    hand.initial_draw(8)
    hand.initial_draw(7)
    hand.draw(3)

    assert hand.get_value() == 18
    for dealer_up_card in range(2,12):
        assert strategy_book.pick_action(hand,dealer_up_card, surrender_available = False) == PlayerDecision.STAND
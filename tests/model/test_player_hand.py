import pytest
from model.player_hand import PlayerHand
from exceptions.hand_exceptions import InitialDrawError


def test_3_2():
    hand = PlayerHand()
    hand.initial_draw(2)
    hand.initial_draw(3)
    assert hand.get_value() == 5

def test_blackjack_11_10():
    hand = PlayerHand()
    hand.initial_draw(10)
    hand.initial_draw(11)
    assert hand.get_value() == 21
    assert not hand.is_bust()
    assert hand.is_black_jack()

def test_blackjack_10_11():
    hand = PlayerHand()
    hand.initial_draw(11)
    hand.initial_draw(10)
    assert hand.get_value() == 21
    assert not hand.is_bust()
    assert hand.is_black_jack()

def test_11_11():
    hand = PlayerHand()
    hand.initial_draw(11)
    hand.initial_draw(11)
    assert not hand.is_bust()
    assert hand.get_value() == 12

def test_11_11_11_11_11():
    hand = PlayerHand()
    hand.initial_draw(11)
    hand.initial_draw(11)
    hand.draw(11)
    hand.draw(11)
    hand.draw(11)
    assert not hand.is_bust()
    assert hand.get_value() == 15

def test_10_6_5():
    hand = PlayerHand()
    hand.initial_draw(10)
    hand.initial_draw(6)
    hand.draw(5)
    assert hand.get_value() == 21
    assert not hand.is_bust()
    assert not hand.is_black_jack()


def test_5_5_11():
    hand = PlayerHand()
    hand.initial_draw(5)
    hand.initial_draw(5)
    hand.draw(11)
    assert hand.get_value() == 21
    assert not hand.is_bust()
    assert not hand.is_black_jack()

def test_11_5_5_11():
    hand = PlayerHand()
    hand.initial_draw(11)
    hand.initial_draw(5)
    hand.draw(5)
    hand.draw(11)
    assert not hand.is_bust()
    assert hand.get_value() == 12

def test_draw_after_five_cards():
    hand = PlayerHand()
    hand.initial_draw(2)
    hand.initial_draw(3)
    hand.draw(2)
    hand.draw(2)
    hand.draw(2)
    assert not hand.is_bust()
    assert hand.get_value() == 11


def test_bust_three_cards_no_ace():
    hand = PlayerHand()
    hand.initial_draw(10)
    hand.initial_draw(6)
    hand.draw(9)

    assert hand.get_value() == 25
    assert hand.is_bust()

def test_bust_with_ace():
    hand = PlayerHand()
    hand.initial_draw(11)
    hand.initial_draw(6)
    hand.draw(10)
    hand.draw(7)

    assert hand.get_value() == 24
    assert hand.is_bust()

def test_soft_12_two_aces():
    hand = PlayerHand()
    hand.initial_draw(11)
    hand.initial_draw(11)
    assert hand.get_value() == 12
    assert not hand.is_bust()
    assert hand.is_soft()

def test_soft_13_two_cards():
    hand = PlayerHand()
    hand.initial_draw(11)
    hand.initial_draw(2)
    assert hand.get_value() == 13
    assert not hand.is_bust()
    assert hand.is_soft()

def test_soft_13_three_aces():
    hand = PlayerHand()
    hand.initial_draw(11)
    hand.initial_draw(11)
    hand.draw(11)
    assert hand.get_value() == 13
    assert hand.is_soft()
    assert not hand.is_bust()

def test_soft_14_four_aces():
    hand = PlayerHand()
    hand.initial_draw(11)
    hand.initial_draw(11)
    hand.draw(11)
    hand.draw(11)
    assert hand.get_value() == 14
    assert not hand.is_bust()
    assert hand.is_soft()

def test_soft_21_ten_aces():
    hand = PlayerHand()
    hand.initial_draw(11)
    hand.initial_draw(11)
    for i in range(9):
        hand.draw(11)
    assert hand.get_value() == 21
    assert not hand.is_bust()
    assert hand.is_soft()

def test_12_aces():
    hand = PlayerHand()
    hand.initial_draw(11)
    hand.initial_draw(11)
    for i in range(10):
        hand.draw(11)
    assert hand.get_value() == 12
    assert not hand.is_bust()
    assert not hand.is_soft()

def test_21_aces():
    hand = PlayerHand()
    hand.initial_draw(11)
    hand.initial_draw(11)
    for i in range(19):
        hand.draw(11)
    assert hand.get_value() == 21
    assert not hand.is_soft()
    assert not hand.is_bust()


def test_22_aces_bust():
    hand = PlayerHand()
    hand.initial_draw(11)
    hand.initial_draw(11)
    for i in range(20):
        hand.draw(11)
    assert hand.get_value() == 22
    assert not hand.is_soft()
    assert hand.is_bust()

def test_2_aces_pair():
    hand = PlayerHand()
    hand.initial_draw(11)
    hand.initial_draw(11)

    assert hand.is_pair()

def test_2_nines_pair():
    hand = PlayerHand()
    hand.initial_draw(9)
    hand.initial_draw(9)

    assert hand.is_pair()

def test_3_of_a_kind_not_pair():
    hand = PlayerHand()
    hand.initial_draw(9)
    hand.initial_draw(9)
    hand.draw(9)

    assert not hand.is_pair()

def test_not_pair():
    hand = PlayerHand()
    hand.initial_draw(9)
    hand.initial_draw(10)

    assert not hand.is_pair()

def test_can_double_on_first_two_cards():
    hand = PlayerHand()
    hand.initial_draw(9)
    hand.initial_draw(10)

    assert hand.can_double

def test_cant_double_on_three_cards():
    hand = PlayerHand()
    hand.initial_draw(5)
    hand.initial_draw(4)
    hand.draw(2)

    assert not hand.can_double
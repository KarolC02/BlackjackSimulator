import pytest
from model.shoe import Shoe
from exceptions.shoe_exceptions import PenetrationNotReachedError

def test_shoe_initialization():
    shoe = Shoe(n_decks=6, penetration=0.75)
    assert shoe.n_decks == 6
    assert shoe.penetration == 0.75
    assert shoe.running_count == 0
    assert shoe.cards_left == 312
    assert shoe.cards_dealt == 0
    assert len(shoe.shoe) == 312

def test_early_shuffle():
    shoe = Shoe(n_decks=6, penetration=0.75)

    with pytest.raises(PenetrationNotReachedError) as excinfo:
        shoe.shuffle()

    assert "penetration" in str(excinfo.value)

def test_deal_card():
    shoe = Shoe(n_decks=6, penetration=0.75)
    shoe_size_before = len(shoe.shoe)
    valid_cards = {2,3,4,5,6,7,8,9,10,11}
    drawn_card = shoe.deal_card()
    assert drawn_card in valid_cards, "Card that has been drawn is not a valid playing card"
    assert len(shoe.shoe) == shoe_size_before - 1, f"Expected shoe size: {shoe_size_before - 1}, actual: {len(shoe.shoe)}"
    assert shoe.cards_left == len(shoe.shoe), f"Cards left: {shoe.cards_left} does not match the size of the shoe: {len(shoe.shoe)}"
    assert shoe.cards_dealt == 1, f"Dealt only 1 card, but shoe.cards_dealt is {shoe.cards_dealt}"

def test_on_time_shuffle():
    decks = 2 
    shoe = Shoe(n_decks = decks, penetration = 0.5)
    for i in range(53):
        shoe.deal_card()
    shoe.shuffle()

    assert len(shoe.shoe) == decks * 52, f"After shuffling expected length of the shoe: {decks*52}, actual: {len(shoe.shoe)}"
    assert shoe.cards_dealt == 0, f"Expected cards dealt after shuffling: {0}, actual: {shoe.cards_dealt}"
    assert shoe.cards_left == len(shoe.shoe)
    assert shoe.running_count == 0, f"Expected running count: {0}, actual: {shoe.running_count}"
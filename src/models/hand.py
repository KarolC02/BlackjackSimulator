from exceptions.hand_exceptions import InitialDrawError, GetValueError, DrawError

class Hand:

    def __init__(self, is_split_hand = False, can_double = True, can_surrender = True, can_draw = True):
        self.cards = []
        self.can_surrender = can_surrender
        self.can_split = False 
        self.can_double = can_double
        self.is_split_hand = is_split_hand
        self.can_draw = can_draw

    def initial_draw(self, initial_card : int ):
        self.cards.append(initial_card)
        if len(self.cards) != 1 and len(self.cards) != 2:
            raise InitialDrawError(len(self.cards))
        
    def draw(self, card : int):
        if len(self.cards) < 2:
            raise DrawError(len(self.cards))
        self.can_double = False
        self.can_surrender = False
        self.can_split = False
        self.cards.append(card)

    def get_value(self) -> int:
        if len(self.cards) < 2:
            raise GetValueError(len(self.cards))
        
        value = sum(self.cards)
        for i in range(self.cards.count(11)):
            if value > 21:
                value -= 10

        return value

    def is_pair(self):
        return len(self.cards)== 2 and self.cards[0] == self.cards[1]

    def is_soft(self):
        total = sum(self.cards)
        for ace in range(self.cards.count(11)):
            total -= 10
        return 11 in self.cards and not total == self.get_value()

    def is_bust(self):
        return self.get_value() > 21

    def is_black_jack(self):
        return len(self.cards) == 2 and 11 in self.cards and 10 in self.cards and not self.is_split_hand

    def disable_surrender(self):
        self.can_surrender = False

    def disable_split(self):
        self.can_split = False

    def disable_double(self):
        self.can_double = False

    def disable_draw(self):
        self.can_draw = False
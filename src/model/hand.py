from exceptions.hand_exceptions import GetValueError

class Hand:
    def __init__(self):
        self.cards = []
        
    def draw(self, card : int):
        self.cards.append(card)

    def get_value(self) -> int:
        value = sum(self.cards)
        for i in range(self.cards.count(11)):
            if value > 21:
                value -= 10

        return value

    def is_bust(self):
        return self.get_value() > 21

    def is_blackjack(self):
        return len(self.cards) == 2 and 11 in self.cards and 10 in self.cards and not self.is_split_hand
    
    def is_soft(self):
        total = sum(self.cards)
        for ace in range(self.cards.count(11)):
            total -= 10
        return 11 in self.cards and not total == self.get_value()
    
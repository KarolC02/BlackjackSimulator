from model.hand import Hand
from exceptions.hand_exceptions import InitialDrawError, GetValueError, DrawError
from utils.logger import logger

class PlayerHand(Hand):
    def __init__(self, bet: int = 1, is_split_hand = False, can_double = True, can_draw = True, use_deviations : bool = False):
        super().__init__()
        self.split_forbidden = False
        self.can_double = can_double
        self.is_split_hand = is_split_hand
        self.can_draw = can_draw 
        self.bet = bet
        self.is_surrendered = False

    def initial_draw(self, initial_card : int ):
        
        self.cards.append(initial_card)
        if len(self.cards) != 1 and len(self.cards) != 2:
            raise InitialDrawError(len(self.cards))
        logger.info(f"Player draws initially a {initial_card}")
        
    def draw(self, card : int):
        if len(self.cards) < 2:
            raise DrawError(len(self.cards))
        logger.info(f"Player draws a {card}")
        self.can_double = False
        self.can_surrender = False
        self.split_forbidden = True
        self.cards.append(card)
    
    def draw_and_disable(self, card : int): # For doubling and resplitting aces
        if len(self.cards) < 2 or (len(self.cards == 1) and self.cards[0] == 11):
            raise DrawError(len(self.cards))
        self.can_double = False
        self.can_surrender = False
        self.split_forbidden = True
        self.can_draw = False
        self.cards.append(card)

    def get_value(self) -> int:
        if len(self.cards) < 2:
            raise GetValueError(len(self.cards))
        
        value = sum(self.cards)
        for i in range(self.cards.count(11)):
            if value > 21:
                value -= 10

        return value

    def add_bet(self, additional_bet : int):
        self.bet += additional_bet

    def get_bet(self):
        return self.bet
    
    def is_splittable(self):
        return self.is_pair() and not self.split_forbidden
    
    def is_pair(self):
        return len(self.cards)== 2 and self.cards[0] == self.cards[1]

    def is_bust(self):
        return self.get_value() > 21
    
    def surrender_hand(self) -> None:
        self.is_surrendered = True

    def disable_surrender(self):
        self.can_surrender = False

    def disable_split(self):
        self.split_forbidden = True

    def disable_double(self):
        self.can_double = False

    def disable_draw(self):
        self.can_draw = False

    def length(self):
        return len(self.cards)

    
    
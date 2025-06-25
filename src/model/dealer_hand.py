from model.hand import Hand
from enums.decisions import DealerDecision

class DealerHand(Hand):
    def __init__(self, s17 : bool = True):
        super().__init__()
        self.s17 = s17

    def select_dealer_move(self):
        if self.get_value() < 17:
            return DealerDecision.HIT
        elif not self.s17 and self.is_soft() and self.get_value() == 17:
            return DealerDecision.HIT
        else:
            return DealerDecision.STAND
        
    def get_upcard(self):
        # This method is to be called only when the dealer has 1 card
        if not len(self.cards == 1):
            raise GetUpCardError(len(self.cards))
        
        return self.cards[0]
        
        

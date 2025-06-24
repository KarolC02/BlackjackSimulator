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
        
        

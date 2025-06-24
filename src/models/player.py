from utils.logger import logger
from exceptions.player_exceptions import NegativeBankrollError

class Player:
    def __init__(self, bankroll : int, spread : int = 1,  betting_unit : int = 1, use_deviations : bool = False, accuracy : float = 1, min_max : bool = False, max_splits : int = 4):
        self.initial_bankroll = bankroll
        self.bankroll = bankroll
        if self.bankroll <= 0:
            raise NegativeBankrollError(self.bankroll)
        self.betting_unit = betting_unit
        self.deviations = use_deviations
        self.accuracy = accuracy
        self.min_max = min_max
        self.max_splits = max_splits
        self.ruin = False

    
    def place_bet(self, true_count : int):
        # TODO - Betting system
        bet = self.get_bet(self,true_count)

        if self.bankroll <= bet:
            logger.info(f"Player is ruined with bankroll: {self.bankroll}")
            self.ruined = True
            return 0
        
        self.bankroll -= bet
        if self.bankroll <= 0:
            raise NegativeBankrollError(self.bankroll)
        return bet
    
    # def make_decision(self, hand : "Hand" true_count : int):

        
from utils.logger import logger
from exceptions.player_exceptions import NegativeBankrollError
from strategy.basic_strategy import BasicStrategy
from model.player_hand import PlayerHand
from enums.decisions import PlayerDecision

class Player:
    def __init__(self, bankroll : int, spread : int = 1,  betting_unit : int = 1, use_deviations : bool = False, accuracy : float = 1, min_max : bool = False, max_splits : int = 4, s17 = True):
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

        if use_deviations:
            pass
        else:
            self.strategy = BasicStrategy(s17)

    
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
    
    def place_double_bet(self, bet : int):
        # TODO - Betting system

        if self.bankroll <= bet:
            logger.info(f"Player can't double as he is ruined with bankroll: {self.bankroll}, and she's trying to double for {self.bet}")
            self.ruined = True
            return 0
        
        self.bankroll -= bet
        if self.bankroll <= 0:
            raise NegativeBankrollError(self.bankroll)
        return bet
    
    def place_insurance_bet(self, bet : int):
        # TODO - Betting system

        if self.bankroll <= bet:
            logger.info(f"Player is ruined with bankroll: {self.bankroll}")
            self.ruined = True
            return 0
        
        self.bankroll -= bet
        if self.bankroll <= 0:
            raise NegativeBankrollError(self.bankroll)
        return bet
    
    def get_correct_action(self, player_hand : PlayerHand, dealer_up_card : int,  true_count : int, surrender_avaiable : bool = True):
        return self.strategy.pick_action(player_hand, dealer_up_card, true_count, surrender_avaiable)
    
    def get_take_insurance(self, dealer_upcard : int , deviations : bool = False, true_count : int = 0):
        if dealer_upcard == 11 and deviations and true_count >= 3:
            return True
        
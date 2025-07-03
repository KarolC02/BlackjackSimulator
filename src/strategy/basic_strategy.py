from enums.decisions import PlayerDecision
from model.player_hand import PlayerHand
from exceptions.hand_exceptions import SurrenderWithMoreThanTwoCardsError, \
SplitWithMoreThanTwoCardsError, SplitWithTwoDifferentCardsError, SoftHandException, DoubleWithMoreThanTwoCardsError, \
NoActionChosenError
from utils.logger import logger
class BasicStrategy():
    def __init__(self, s17 : bool = True):
        self.s17 = s17

    def pick_action(self, player_hand : PlayerHand, dealer_up_card : int,  true_count : int = 0, surrender_available : bool = True, split_available = True):
        #############################################################
        ######################### Surrender #########################
        #############################################################
        if not player_hand.can_draw:
            logger.info("This hand was likely created through splitting aces or doubling, only can stand")
            return PlayerDecision.STAND
        if surrender_available and not player_hand.is_soft(): # You never surrender a soft hand
            if not player_hand.length() == 2:
                raise SurrenderWithMoreThanTwoCardsError(player_hand.length())
            if player_hand.get_value() == 16 and player_hand.is_splittable() and dealer_up_card == 10: # 8,8 vs 10
                return PlayerDecision.SURRENDER
            if player_hand.get_value() == 16 and not player_hand.is_splittable() and dealer_up_card == 10: # 16 vs 10
                return PlayerDecision.SURRENDER
            if player_hand.get_value() == 16 and not player_hand.is_splittable() and dealer_up_card == 9: # 10,6 vs 9
                return PlayerDecision.SURRENDER
            if player_hand.get_value() == 15 and dealer_up_card == 10:
                return PlayerDecision.SURRENDER
            if player_hand.get_value() == 14 and player_hand.is_splittable() and dealer_up_card == 10: # 7,7 vs 10
                return PlayerDecision.SURRENDER
            if player_hand.get_value() == 14 and not player_hand.is_splittable() and dealer_up_card == 10: # 14 vs 10
                return PlayerDecision.SURRENDER
            
        #############################################################
        #########################   Splits  #########################
        #############################################################
        if player_hand.is_splittable() and split_available:
            if not player_hand.length() == 2:
                raise SplitWithMoreThanTwoCardsError(player_hand.length())
            if player_hand.cards[0] != player_hand.cards[1]:
                raise SplitWithTwoDifferentCardsError(player_hand.cards[0], player_hand.cards[1])
            if player_hand.get_value() == 4 and 2 <= dealer_up_card <= 7:
                return PlayerDecision.SPLIT
            if player_hand.get_value() == 6 and 2 <= dealer_up_card <= 7:
                return PlayerDecision.SPLIT
            if player_hand.get_value() == 8 and 5 <= dealer_up_card <= 6:
                return PlayerDecision.SPLIT
            if player_hand.get_value() == 12 and player_hand.cards == [6,6] and 2 <= dealer_up_card <= 6:
                return PlayerDecision.SPLIT
            if player_hand.get_value() == 14 and 2 <= dealer_up_card <= 7:
                return PlayerDecision.SPLIT
            if player_hand.get_value() == 16 and 2 <= dealer_up_card <= 9:
                return PlayerDecision.SPLIT
            if player_hand.get_value() == 18 and 2 <= dealer_up_card <= 9 and dealer_up_card != 7:
                return PlayerDecision.SPLIT
            if player_hand.get_value() == 12 and player_hand.cards == [11,11] and 2 <= dealer_up_card <= 10:
                return PlayerDecision.SPLIT
            
        #############################################################
        #######################  Soft Hands  ########################
        #############################################################
        if player_hand.is_soft():
            if 11 not in player_hand.cards:
                raise SoftHandException(player_hand)
            if player_hand.get_value() >= 19:
                return PlayerDecision.STAND
            if player_hand.get_value() == 18:
                if dealer_up_card in {3,4,5,6} and player_hand.can_double:
                    return PlayerDecision.DOUBLE
                if dealer_up_card in {3,4,5,6} and not player_hand.can_double:
                    return PlayerDecision.STAND
                if dealer_up_card in {2,7}:
                    return PlayerDecision.STAND
                else:
                    return PlayerDecision.HIT
            if player_hand.get_value() == 17 and 3 <= dealer_up_card <= 6 and player_hand.can_double:
                return PlayerDecision.DOUBLE
            if player_hand.get_value() == 16 and 4 <= dealer_up_card <= 6 and player_hand.can_double:
                return PlayerDecision.DOUBLE
            if player_hand.get_value() == 15 and 4 <= dealer_up_card <= 6 and player_hand.can_double:
                return PlayerDecision.DOUBLE
            if player_hand.get_value() == 14 and 5 <= dealer_up_card <= 6 and player_hand.can_double:
                return PlayerDecision.DOUBLE     
            if player_hand.get_value() == 13 and 5 <= dealer_up_card <= 6 and player_hand.can_double:
                return PlayerDecision.DOUBLE    
            else:
                return PlayerDecision.HIT 
            
        #############################################################
        ####################### Hard Doubles ########################
        #############################################################
        if player_hand.can_double:
            if not player_hand.length() == 2:
                raise DoubleWithMoreThanTwoCardsError(player_hand.length())
            if player_hand.get_value() == 11 and 2 <= dealer_up_card <= 9:
                return PlayerDecision.DOUBLE
            if player_hand.get_value() == 10 and 2 <= dealer_up_card <= 9:
                return PlayerDecision.DOUBLE
            if player_hand.get_value() == 9 and 3 <= dealer_up_card <= 6:
                return PlayerDecision.DOUBLE
        
        #############################################################
        ######################  Hard Hit/Stand ######################
        #############################################################
        if player_hand.get_value() <= 11:
            return PlayerDecision.HIT
        if player_hand.get_value() == 12:
            if ( 4 <= dealer_up_card <= 6 ):
                return PlayerDecision.STAND
            else:
                return PlayerDecision.HIT
        if 13 <= player_hand.get_value() <= 16:
            if ( 2 <= dealer_up_card <= 6 ):
                return PlayerDecision.STAND
            else:
                return PlayerDecision.HIT
        if  17 <= player_hand.get_value():
            return PlayerDecision.STAND
        
        raise NoActionChosenError(player_hand.cards, dealer_up_card)

from exceptions.base import BlackjackError

class InitialDrawError(BlackjackError):
    def __init__(self, n_of_cards : int):
        super().__init__(f"Wrong usage of initial draw, player drew using the inital draw to {n_of_cards} cards")


class GetValueError(BlackjackError):
    def __init__(self, n_of_cards : int):
        super().__init__(f"Called get_value() on a hand with {n_of_cards} cards")

class DrawError(BlackjackError):
    def __init__(self, n_of_cards : int):
        super().__init__(f"Wrong usage of draw, player drew using the draw method to {n_of_cards} cards")

class SurrenderWithMoreThanTwoCardsError(BlackjackError):
    def __init__(self, n_of_cards : int):
        super().__init__(f"The hand with {n_of_cards} was mistakenly labeled as being able to surrender")

class DoubleWithMoreThanTwoCardsError(BlackjackError):
    def __init__(self, n_of_cards : int):
        super().__init__(f"The hand with {n_of_cards} was mistakenly labeled as being able to double")

class SplitWithMoreThanTwoCardsError(BlackjackError):
    def __init__(self, n_of_cards : int):
        super().__init__(f"The hand with {n_of_cards} was mistakenly labeled as being able to split")

class SplitWithTwoDifferentCardsError(BlackjackError):
    def __init__(self, card1: int, card2 : int):
        super().__init__(f"the following hand: [{card1},{card2}] has been mistakenly labeled as being able to split")

class SoftHandException(BlackjackError):
    def __init__(self, hand_cards : list):
        super().__init__(f"the following hand: [{hand_cards}] has been mistakenly labeled as a soft hand")

class NoActionChosenError(BlackjackError):
    def __init__(self, player_hand_cards : list, dealer_up_card : int):
        super().__init__(f"No action was choses for player hand : {player_hand_cards} and dealer upcard: {dealer_up_card}")

    

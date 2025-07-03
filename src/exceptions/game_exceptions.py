from exceptions.base import BlackjackError

class SurrenderNotAvailableError(BlackjackError):
    def __init__(self):
        super().__init__(f"Player choose to surrender even though surrender_available is set to False")

class SplitIntoMoreThanFiveHandsError(BlackjackError):
    def __init__(self):
        super().__init__(f"Player choose to split with 4 or more hands in game")

class SplitTwoDifferenCardsChoiceError(BlackjackError):
    def __init__(self):
        super().__init__(f"Player choose to split with 2 different cards")

class SplitTwoDifferenCardsChHandCountMismatchErroroiceError(BlackjackError):
    def __init__(self, len_hands_to_resolve : int, hands_count : int):
        super().__init__(f"Length of hands_to_resolve is {len_hands_to_resolve}, but the hands_count is {hands_count}")
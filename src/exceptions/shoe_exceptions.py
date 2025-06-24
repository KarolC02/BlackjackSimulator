from exceptions.base import BlackjackError

class InvalidShoeSizeError(BlackjackError):
    def __init__(self, expected : int , actual : int, n_decks : int):
        super().__init__(f"With {n_decks} decks, expected shoe size is {expected}, actual : {actual}")
        self.expected = expected
        self.actual = actual
        self.n_decks = n_decks

class PenetrationNotReachedError(BlackjackError):
    def __init__(self, current_penetration : float, deck_penetration : float):
        super().__init__(f"Shuffled to early, current penetration : {current_penetration}, deck penetration : {deck_penetration}")
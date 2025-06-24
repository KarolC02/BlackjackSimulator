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
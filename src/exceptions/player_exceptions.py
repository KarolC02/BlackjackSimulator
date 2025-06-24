from exceptions.base import BlackjackError

class NegativeBankrollError(BlackjackError):
    def __init__(self, current_bankroll : float):
        super().__init__(f"Error: Player bankroll is negative:{current_bankroll}")

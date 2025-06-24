from enum import Enum, auto

class PlayerDecision(Enum):
    STAND = auto()
    HIT = auto()
    DOUBLE = auto()
    SPLIT = auto()
    SURRENDER = auto()
    INSURANCE = auto()
    NOINSURANCE = auto()


class DealerDecision(Enum):
    STAND = auto()
    HIT = auto()

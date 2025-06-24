from random import shuffle
from utils.logger import logger
from exceptions.shoe_exceptions import InvalidShoeSizeError, PenetrationNotReachedError

class Shoe:
    def __init__(self, n_decks : int, penetration : float):
        self.n_decks = n_decks
        self.penetration = penetration

        self.create_shoe()



    def create_shoe(self) -> None:
        self.running_count = 0
        self.cards_dealt = 0
        self.shoe = self.n_decks * 4 *  [2,3,4,5,6,7,8,9,10,10,10,10,11]
        shuffle(self.shoe)
        self.cards_left = len(self.shoe)

        if len(self.shoe) != self.cards_left:
            raise InvalidShoeSizeError(52 * self.n_decks, self.cards_left, self.n_decks)

        logger.debug(f"Shoe after creating : {self.shoe[0:10]}...")

    def get_current_penetration(self) -> float:
        return (float) (self.cards_dealt)/(52 * self.n_decks)
    
    def shuffle(self):

        if not self.get_current_penetration() >= self.penetration:
            raise PenetrationNotReachedError(self.get_current_penetration(), self.penetration)

        self.create_shoe()
        
    def deal_card(self) -> int:
        card = self.shoe.pop()
        self.cards_dealt += 1
        self.cards_left -= 1

        return card


        



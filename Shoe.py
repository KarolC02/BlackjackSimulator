class Shoe:
    def __init__(self, n_decks : int, penetration : float):
        self.n_decks = n_decks
        self.penetration = penetration
        self.running_count = 0
        self.cards_left = 52 * self.n_decks
        self.cards_dealt = 0

        self.shoe = (self.n_decks * 4) *  [2,3,4,5,6,7,8,9,10,10,10,10,11]
        assert self.shoe.length == self.cards_left, "The number of cards does not match the theoretical value"

    def shuffle(self):
        assert (float) (self.cards_dealt)/(52 * self.n_decks) >= self.penetration


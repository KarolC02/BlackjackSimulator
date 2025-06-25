from model.player import Player
from model.dealer_hand import DealerHand
from model.player_hand import PlayerHand
from model.shoe import Shoe
from utils.logger import logger
from enums.decisions import PlayerDecision, DealerDecision
class Game():
    def __init__(self, player_bankroll : int = 10000, player_betting_unit : int = 30, use_deviations : bool = False, nPlayers : int = 1, s17 : bool = True, blackjack_pays : float = 1.5, n_decks : int = 6, penetration : float = 0.75, play_hands : int = 100):
        self.player = Player(bankrol = player_bankroll, betting_unit = player_betting_unit)
        self.shoe = Shoe(n_decks = n_decks, penetration=penetration)
        self.initial_player_bankroll = player_bankroll
        self.player_betting_unit = player_betting_unit
        self.blackjack_pays = blackjack_pays
        self.use_deviations = use_deviations
        self.hands_played = 0
        self.shoes_played = 0
        self.player_hands = set()
        self.surrender_available = True
        self.play_hands = play_hands

    def play_game(self):
        

        while self.hands_played < self.play_hands:
            if self.shoe.needs_reshuffling():
                self.shoes_played += 1
                logger.info(f"Shoe Finished! Total shoes played : {self.shoes_played}")

            self.player_hands = set()
            self.surrender_available = True

            # Player places bet
            player_bet = self.player.place_bet()
            player_hand = PlayerHand(player_bet)
            dealer_hand = DealerHand()

            # Initial Draw
            player_hand.initial_draw(self.shoe.deal_card())
            dealer_hand.draw(self.shoe.deal_card())
            player_hand.initial_draw(self.shoe.deal_card())

            self.player_hands.add(player_hand)

            dealer_up_card = dealer_hand.get_upcard()
            surrender_available = True
            # Insurance?
            take_insurance = self.player.get_take_insurance(dealer_up_card, self.use_deviations, self.shoe.get_true_count())
            insurance_bet = 0
            if take_insurance:
                insurance_bet = self.player.place_insurance_bet()

                    
            # Blackjack Handling:
            if player_hand.is_black_jack():
                self.player.bankroll += player_hand.get_bet()
                if dealer_up_card in {10,11}:
                    dealer_hand.draw(self.shoe.deal_card())
                    if dealer_hand.is_black_jack():
                        return
                self.player.bankroll += self.blackjack_pays * player_hand.get_bet()
            else:
                self.play_hand(player_hand, dealer_up_card, surrender_available)

            self.hands_played += 1
        

    def play_hand(self, hand : PlayerHand, dealer_up_card : int):

        # If this hand is a results of a split, draw one more card up to 2, if this hand is a result of splitting aces, draw and disable
        if len(hand.cards) == 1 and hand.cards[0] != 11:
            hand.draw(self.shoe.deal_card())
        if len(hand.cards) == 1 and hand.cards[0] == 1:
            hand.draw_and_disable(self.shoe.deal_card())

        while True:
            player_decision = self.player.get_correct_action(hand, dealer_up_card, self.shoe.get_true_count(), self.surrender_available)
            if player_decision == PlayerDecision.SURRENDER:
                self.is_surrendered = True
                return
            elif player_decision == PlayerDecision.SPLIT:
                self.surrender_available = False
                self.player_hands.remove(hand)
                assert hand.cards[0] == hand.cards[1]
                new_hand1 = PlayerHand()
                new_hand2 = PlayerHand()

                new_hand1.initial_draw(hand.cards[0])
                new_hand2.initial_draw(hand.cards[1])

                self.player_hands.add(new_hand1)
                self.player_hands.add(new_hand2)

                if len(self.player_hands == 4):
                    new_hand1.disable_split()
                    new_hand2.disable_split()
                if len(self.player_hands > 4):
                    raise Exception("Splitted into more that 4 hands")
                
            elif player_decision == PlayerDecision.DOUBLE:
                self.surrender_available = False
                hand.add_bet(self.player.place_double_bet(hand.get_bet()))
                hand.draw_and_disable(self.shoe.deal_card())
                if hand.is_bust():
                    return

            elif player_decision == PlayerDecision.HIT:
                self.surrender_available = False
                hand.draw(self.shoe.deal_card())
                if hand.is_bust():
                    return

            elif player_decision == PlayerDecision.STAND:
                return
        

        
    def shuffle_shoe(self):
        self.shoe.shuffle()
        assert self.shoe.running_count == 0
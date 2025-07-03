from model.player import Player
from model.dealer_hand import DealerHand
from model.player_hand import PlayerHand
from model.shoe import Shoe
from utils.logger import logger
from enums.decisions import PlayerDecision, DealerDecision
from exceptions.game_exceptions import SurrenderNotAvailableError, SplitIntoMoreThanFiveHandsError, SplitTwoDifferenCardsChoiceError, HandCountMismatchError

class Game():
    def __init__(self, player_bankroll : int = 10000, player_betting_unit : int = 30, use_deviations : bool = False, nPlayers : int = 1, s17 : bool = True, blackjack_pays : float = 1.5, n_decks : int = 6, penetration : float = 0.75):
        self.player = Player(bankrol = player_bankroll, betting_unit = player_betting_unit)
        self.shoe = Shoe(n_decks = n_decks, penetration=penetration)
        self.initial_player_bankroll = player_bankroll
        self.player_betting_unit = player_betting_unit
        self.blackjack_pays = blackjack_pays
        self.use_deviations = use_deviations
        self.hands_played = 0
        self.shoes_played = 0

        # Reset each round
        self.player_initial_hand = []
        self.dealer_hand = DealerHand()
        self.hands_to_resolve = []
        self.hands_to_play = []
        self.hands_count = 0
        self.split_available = True
        self.surrender_available = True
        self.take_insurance = False
        self.insurance_bet = 0


    def play_rounds(self, rounds : int = 100):
        

        while self.hands_played < rounds:

            self.reshuffle_shoe_if_needed()
            self.reset_round()
            self.deal_initial_cards()
            self.decide_on_insurance()

                    
            # Blackjack Handling:
            if self.player_initial_hand.is_black_jack():
                # get the original bet back
                self.player.bankroll += self.player_initial_hand.get_bet()
                if self.dealer_hand.get_upcard() in {10,11}:
                    self.dealer_hand.draw(self.shoe.deal_card())
                    if self.dealer_hand.is_black_jack():
                        return
                self.player.bankroll += self.blackjack_pays * self.player_initial_hand.get_bet()

            else:
                while len(self.hands_to_play) > 0:
                    hand_to_play = self.hands_to_play.pop()
                    self.play_hand(hand_to_play, self.dealer_hand.get_upcard())


            # TODO - resolve hands
            if len(self.hands_to_resolve) != self.hands_played:
                raise HandCountMismatchError(self.hands_to_resolve, self.hands_played)


            self.resolve_bets()

            self.hands_played += 1
        

    def play_hand(self, hand : PlayerHand, dealer_up_card : int):

        # If this hand is a results of a split, draw one more card up to 2, if this hand is a result of splitting aces, draw and disable

        if len(hand.cards) == 1:
            if hand.cards[0] != 11:
                hand.draw(self.shoe.deal_card())
            else: # If it's an ace after splitting, draw just one cards
                hand.draw_and_disable(self.shoe.deal_card())
                self.hands_to_resolve.add(hand)
                return


        while True:
            player_decision = self.player.get_correct_action(hand, dealer_up_card, self.shoe.get_true_count(), self.surrender_available, split_available = self.split_available)

            if player_decision == PlayerDecision.SURRENDER:
                if not self.surrender_available:
                    raise SurrenderNotAvailableError()
                hand.is_surrendered = True
                self.hands_to_resolve.add(hand)
                return
            
            elif player_decision == PlayerDecision.SPLIT:

                if not self.hands_count < 4:
                    raise SplitIntoMoreThanFiveHandsError()
                if not hand.cards[0] == hand.cards[1]:
                    raise SplitTwoDifferenCardsChoiceError()

                original_bet = hand.get_bet()

                new_hand1 = PlayerHand(original_bet)
                new_hand2 = PlayerHand(self.player.place_double_bet(original_bet))

                new_hand1.initial_draw(hand.cards[0])
                self.surrender_available = False
                new_hand2.initial_draw(hand.cards[1])

                self.player_hands.add(new_hand1)
                self.player_hands.add(new_hand2)

                hands += 1

                if len(self.player_hands == 4):
                    self.split_available = False
                if len(self.player_hands > 4):
                    raise SplitIntoMoreThanFiveHandsError()
                
            elif player_decision == PlayerDecision.DOUBLE:
                self.surrender_available = False
                hand.add_bet(self.player.place_double_bet(hand.get_bet()))
                hand.draw_and_disable(self.shoe.deal_card())
                self.hands_to_resolve.add(hand)
                return

            elif player_decision == PlayerDecision.HIT:
                self.surrender_available = False
                hand.draw(self.shoe.deal_card())
                if hand.is_bust():
                    self.hands_to_resolve.add(hand)
                    return

            elif player_decision == PlayerDecision.STAND:
                self.hands_to_resolve.add(hand)
                return
        

    def reshuffle_shoe_if_needed(self) -> None:
        if self.shoe.needs_reshuffling():
            self.shoes_played += 1
            logger.info(f"Shoe Finished! Total shoes played : {self.shoes_played}")
            self.shoe.shuffle()

    def reset_round(self) -> None:
        self.player_initial_hand = []
        self.dealer_hand = []
        self.hands_to_resolve = []
        self.hands_to_play = []
        self.hands_count = 0
        self.split_available = True
        self.surrender_available = True
        self.take_insurance = False
        self.insurance_bet = 0



    def deal_initial_cards(self) -> None:
        # Player places bet
        player_bet = self.player.place_bet()


        player_hand = PlayerHand(player_bet)
        dealer_hand = DealerHand()

        # Initial Draw
        player_hand.initial_draw(self.shoe.deal_card())
        dealer_hand.draw(self.shoe.deal_card())
        player_hand.initial_draw(self.shoe.deal_card())

        self.hands_to_resolve.add(player_hand)
        hands += 1

    def decide_on_insurance(self) -> None:
        # Insurance?
        take_insurance = self.player.get_take_insurance(self.dealer_hand.get_upcard(), self.use_deviations, self.shoe.get_true_count())
        if take_insurance:
            self.insurance_bet = self.player.place_insurance_bet()
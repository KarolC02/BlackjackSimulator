from model.player import Player
from model.dealer_hand import DealerHand
from model.player_hand import PlayerHand
from model.shoe import Shoe
from utils.logger import logger
from enums.decisions import PlayerDecision, DealerDecision
from exceptions.game_exceptions import SurrenderNotAvailableError, SplitIntoMoreThanFiveHandsError, SplitTwoDifferenCardsChoiceError, HandCountMismatchError, InsuranceTakenWithNoDealerAceError

class Game():
    def __init__(self, player_bankroll : int = 10000, player_betting_unit : int = 30, use_deviations : bool = False, nPlayers : int = 1, s17 : bool = True, blackjack_pays : float = 1.5, n_decks : int = 6, penetration : float = 0.75):
        self.player = Player(bankroll = player_bankroll, betting_unit = player_betting_unit)
        self.shoe = Shoe(n_decks = n_decks, penetration=penetration)
        self.initial_player_bankroll = player_bankroll
        self.player_betting_unit = player_betting_unit
        self.blackjack_pays = blackjack_pays
        self.use_deviations = use_deviations
        self.hands_played = 0
        self.shoes_played = 0

        # Reset each round
        self.reset_round()

    def reset_round(self) -> None:
        self.player_initial_hand : PlayerHand = PlayerHand()
        self.dealer_hand : DealerHand = DealerHand()
        self.hands_to_resolve : list[PlayerHand] = list()
        self.hands_to_play : list[PlayerHand] = list()
        self.hands_count : int = 0
        self.split_available : bool = True
        self.surrender_available : bool = True
        self.take_insurance : bool = False
        self.insurance_bet : int = 0


    def play_rounds(self, rounds : int = 100):
        while self.hands_played < rounds:
            self.play_round()

    def play_round(self):
        self.reshuffle_shoe_if_needed()
        self.reset_round()
        self.deal_initial_cards()
        self.decide_on_insurance()
        while len(self.hands_to_play) > 0:
            hand_to_play = self.hands_to_play.pop()
            self.play_hand(hand_to_play, self.dealer_hand.get_upcard())

        self.resolve_bets()
        self.hands_played += 1
        self.reset_round()

    
    def resolve_bets(self) -> None:
        if len(self.hands_to_resolve) != self.hands_played:
                raise HandCountMismatchError(self.hands_to_resolve, self.hands_played)
        
        # Handle Insurance
        if self.dealer_hand.is_blackjack():
            # Handle Insurance
            if self.insurance_bet > 0:
                if self.dealer_hand[0] != 11:
                    raise InsuranceTakenWithNoDealerAceError
                self.player.win_insurance_bet(self.insurance_bet)

        for hand in self.hands_to_resolve:
            # Surrender
            if hand.is_surrendered():
                self.player.resolve_surrender_bet(hand)
            # BlackJack
            elif hand.is_blackjack():
                if not self.dealer_hand.is_blackjack():
                    self.player.win_blackjack_hand(hand, self.blackjack_pays)
                else:
                    self.player.get_original_bet_back(hand)
            # Bust
            elif hand.is_bust(): # The best is already taken from the player
                continue
            # Player vs Dealer
            else:
                if self.dealer_hand.is_blackjack():
                    assert not hand.is_blackjack(), "The situation in which the player and the dealer has blackjack should have been resolved earlier"
                    continue # The player pays the best as the cards are dealt, no need to do anything if the player loses
                if self.dealer_hand.get_value() == hand.get_value():
                    self.player.get_original_bet_back(hand)
                if hand.get_value() > self.dealer_hand.get_value():
                    self.player.win_hand(hand)
                else: # self.dealer_hand.get_value() < hand.get_value()
                    continue

    def play_hand(self, hand : PlayerHand, dealer_up_card : int):

        # If this hand is a results of a split, draw one more card up to 2, if this hand is a result of splitting aces, draw and disable

        if len(hand.cards) == 1:
            if hand.cards[0] != 11:
                hand.draw(self.shoe.deal_card())
            else: # If it's an ace after splitting, draw just one card
                hand.draw_and_disable(self.shoe.deal_card())
                self.hands_to_resolve.append(hand)
                return


        while True:
            player_decision = self.player.get_correct_action(hand, dealer_up_card, self.shoe.get_true_count(), self.surrender_available, split_available = self.split_available)

            if player_decision == PlayerDecision.SURRENDER:
                if not self.surrender_available:
                    raise SurrenderNotAvailableError()
                hand.surrender_hand()
                self.hands_to_resolve.append(hand)
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

                self.player_hands.append(new_hand1)
                self.player_hands.append(new_hand2)

                hands += 1

                if len(self.player_hands == 4):
                    self.split_available = False
                if len(self.player_hands > 4):
                    raise SplitIntoMoreThanFiveHandsError()
                
            elif player_decision == PlayerDecision.DOUBLE:
                self.surrender_available = False
                hand.add_bet(self.player.place_double_bet(hand.get_bet()))
                hand.draw_and_disable(self.shoe.deal_card())
                self.hands_to_resolve.append(hand)
                return

            elif player_decision == PlayerDecision.HIT:
                self.surrender_available = False
                hand.draw(self.shoe.deal_card())
                if hand.is_bust():
                    self.hands_to_resolve.append(hand)
                    return

            elif player_decision == PlayerDecision.STAND:
                self.hands_to_resolve.append(hand)
                return
        

    def reshuffle_shoe_if_needed(self) -> None:
        if self.shoe.needs_reshuffling():
            self.shoes_played += 1
            logger.info(f"Shoe Finished! Total shoes played : {self.shoes_played}")
            self.shoe.shuffle()

    def deal_initial_cards(self) -> None:
        # Player places bet
        player_bet = self.player.place_bet(self.shoe.get_true_count())


        player_hand = PlayerHand(player_bet)
        dealer_hand = DealerHand()

        # Initial Draw
        player_hand.initial_draw(self.shoe.deal_card())
        self.dealer_hand.draw(self.shoe.deal_card())
        player_hand.initial_draw(self.shoe.deal_card())

        self.hands_to_play.append(player_hand)
        self.hands_count += 1

    def decide_on_insurance(self) -> None:
        # Insurance?
        take_insurance = self.player.get_take_insurance(self.dealer_hand.get_upcard(), self.use_deviations, self.shoe.get_true_count())
        if take_insurance:
            self.insurance_bet = self.player.place_insurance_bet(self.player_initial_hand)
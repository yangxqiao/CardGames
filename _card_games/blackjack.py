import random


SUITS = ['hearts', 'spades', 'diamonds', 'clubs']
RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']

INIT_NUM_CARD_IN_HAND = 2


def generate_human_players(*names):
    human_players = []
    for name in names:
        player = Human(name)
        human_players.append(player)
    return human_players


def generate_robot_players(num_robot):
    robot_players = []
    for i in range(num_robot):
        player = Robot(name="robot%s" % i)
        robot_players.append(player)
    return robot_players


def make_deck(deck):
    for suit in SUITS:
        for rank in RANKS:
            deck.add_cards(Card(suit, rank))


def input_yes_or_no(question):
    invalid_answer = True
    while invalid_answer:

        user_choice = input(question)

        try:
            return is_yes_or_no(user_choice)
        except ValueError:
            print("Please provide a valid answer.")


def is_yes_or_no(text):

    text = text.lower()
    if text in ['y', 'yes', 'yup']:
        return True

    elif text in ['n', 'no', 'nope']:
        return False

    else:
        raise ValueError("The string cannot parse yes or no")


class Card:
    def __init__(self, suit, rank, is_face_up=False):
        if suit not in SUITS:
            raise ValueError

        if rank not in RANKS:
            raise ValueError

        if is_face_up not in [False, True]:
            raise ValueError

        self.suit = suit
        self.rank = rank
        self.is_face_up = is_face_up

    def flip(self):
        self.is_face_up = not self.is_face_up

    def __repr__(self):
        return str(self.rank)


class CardCollection:
    def __init__(self):
        self.cards = []

    def _add_card(self, new_card):
        if not isinstance(new_card, Card):
            raise TypeError

        self.cards.append(new_card)

    def add_cards(self, *new_cards):
        for card in new_cards:
            self._add_card(card)

    def pop_card(self):
        if self.cards == []:
            raise IndexError("This CardCollection is empty now.")
        return self.cards.pop()

    def flip_card(self, card_idx):
        if type(card_idx) is int and 0 <= card_idx < self.num_of_cards():
            self.cards[card_idx].flip()

        else:
            raise IndexError

    def shuffle(self):
        random.shuffle(self.cards)

    def num_of_cards(self):
        return len(self.cards)

    def clear(self):
        self.cards.clear()

    def __getitem__(self, idx):
        return self.cards[idx]

    def __repr__(self):
        return str(self.cards)


class BlackJackPlayer:

    def __init__(self, name):
        if not isinstance(name, str):
            raise ValueError

        self.name = name
        self.hand = CardCollection()

    @property
    def points(self):

        num_of_aces = 0
        total_value = 0

        # calculate the total scores with Ace counted as 11
        for i in range(self.hand.num_of_cards()):
            total_value += self._get_card_value_with_rank(i)
            if self._get_card_value_with_rank(i) == 11:
                num_of_aces += 1

        # find the highest score under 21 counting Aces as 1s
        for i in range(num_of_aces):
            if total_value > 21:
                total_value -= 10
        return total_value

    def _get_card_value_with_rank(self, card_idx):

        rank = self.hand[card_idx].rank

        if rank == 'A':
            return 11
        elif rank in ['J', 'Q', 'K']:
            return 10
        else:
            return int(rank)

    def is_choose_to_hit(self):
        raise NotImplementedError("This function is meant to be implemented in a subclass")

    def print_status(self):
        print("%s's score is %s: %s" % (self.name, self.points, self.hand))

    def __repr__(self):
        return str(self.hand)


class Human(BlackJackPlayer):

    def __init__(self, name):
        BlackJackPlayer.__init__(self, name)

    def is_choose_to_hit(self):

        if self.points > 21:
            return False

        else:
            invalid_answer = True

            while invalid_answer:
                player_decision = input("Hi, %s. Type 'h' to hit and 's' to stay:\n" % self.name).lower()
                if player_decision == 'h':
                    return True
                elif player_decision == 's':
                    return False
                else:
                    print("Please provide a valid answer.")


class Robot(BlackJackPlayer):
    def __init__(self, name):
        BlackJackPlayer.__init__(self, name)

    def is_choose_to_hit(self):
        total_value = self.points
        if total_value < 17:
            return True

        elif 17 <= total_value:
            return False


class BlackJackGame:
    # pass in a list of players
    # pass in one dealer
    def __init__(self, dealer, players):
        self._dealer = dealer
        self._players = players
        self._deck = CardCollection()

    def num_of_players(self):
        return 1 + len(self._players)

    def _init_deck(self):
        self._clear_deck()

        if self.num_of_players() * 11 >= self._deck.num_of_cards():
            num_of_deck = self.num_of_players() * 11 // 52 + 1

            for _ in range(num_of_deck):
                make_deck(self._deck)

            self._deck.shuffle()

    def _init_players_hand(self):
        self._clear_hands()

        for player in self._players:
            for _ in range(INIT_NUM_CARD_IN_HAND):
                player.hand.add_cards(self._deck.pop_card())

        for _ in range(INIT_NUM_CARD_IN_HAND):
            self._dealer.hand.add_cards(self._deck.pop_card())
            self._dealer.hand.flip_card(0)

    def _clear_hands(self):
        for player in self._players + [self._dealer]:
            player.hand.clear()

    def _clear_deck(self):
        self._deck.clear()

    def _evaluate_results(self):

        for player in self._players:
            if ((self._dealer.points > 21 and player.points <= 21)
                    or (self._dealer.points < player.points <= 21)):
                print("%s won with score %s" % (player.name, player.points))

            else:
                print("%s lost with score %s" % (player.name, player.points))

    def _do_turn(self, player):

        player.print_status()

        while player.is_choose_to_hit():
            player.hand.add_cards(self._deck.pop_card())
            player.print_status()

    def run(self):

        keep_playing = True
        while keep_playing:

            self._init_deck()
            self._init_players_hand()

            for player in self._players + [self._dealer]:
                self._do_turn(player)

            self._evaluate_results()

            keep_playing = input_yes_or_no("Do you want to keep playing?\n")


if __name__ == '__main__':

    dealer = Robot("Dealer")
    human_player = generate_human_players('Yang', 'Kat')
    robot_player = generate_robot_players(20)
    players = human_player + robot_player

    lets_play_game = BlackJackGame(dealer, players)
    lets_play_game.run()

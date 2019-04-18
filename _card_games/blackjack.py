import random

my_card = {
    'number': ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A'],
    'type': ['hearts', 'spades', 'diamonds', 'clubs'],
    'value': [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11],
}

num_of_total_dealt_cards = 0


class Card:
    def __init__(self, total_num_of_cards, my_card):
        self.total_num_of_cards = total_num_of_cards
        self.my_card = my_card
        self.cards = []

    def shuffle_cards(self):
        for i in range(self.total_num_of_cards):
            self.cards.append(i)
        random.shuffle(self.cards)


class Person:
    def __init__(self, name, my_card):
        self.name = name
        self.hand = []
        self.my_card = my_card

    def receive_card(self, *args):
        for card_id in args:
            self.hand.append(card_id)

    def get_num_card_in_hand(self):
        return len(self.hand)

    def print_card(self, card_id):
        type_of_card = self.my_card['type'][card_id // 13]
        num_on_card = self.my_card['number'][card_id % 13]
        return "%s-%s " % (type_of_card, num_on_card)

    def print_hand(self):
        target_str = ""
        for i in range(len(self.hand)):
            target_str = target_str + self.print_card(self.hand[i]) + " "

        return target_str

    def get_card_value(self, card_id):
        return self.my_card['value'][card_id % 13]

    def get_best_score(self):
        num_of_aces = 0
        total_value = 0
        # calculate the total scores with A counted as 11
        for i in range(self.get_num_card_in_hand()):
            total_value += self.get_card_value(self.hand[i])
            if self.get_card_value(self.hand[i]) == 11:
                num_of_aces += 1
        # calculate for the best case
        for i in range(num_of_aces):
            if total_value > 21:
                total_value -= 10

        return total_value

keep_playing = True
while keep_playing:
    # initialize the card game
    bj = Card(52, my_card)
    bj.shuffle_cards()

    player = Person('Yang', my_card)
    dealer = Person('Robots', my_card)

    dealer.receive_card(bj.cards[1], bj.cards[3])
    player.receive_card(bj.cards[0], bj.cards[2])

    num_of_total_dealt_cards = 4

    print("Dealer: ? %s" % dealer.print_card(dealer.hand[1]))
    print("Player: %s" % player.print_hand())

    # determine player's initial status after getting two cards
    if player.get_best_score() == 21:
        player_status = 's'
    else:
        player_status = input("Type 'h' to hit and 's' to stay:\n")

    # check for if player_status is correct
    correct_input = True
    if player_status != 's' and player_status != 'h':
        correct_input = False
        keep_playing = False

    while correct_input:

        if player_status == 's':

            while dealer.get_best_score() < 17:
                dealer.receive_card(bj.cards[num_of_total_dealt_cards])
                num_of_total_dealt_cards += 1

            print("Dealer: %s" % dealer.print_hand())

            if 17 <= dealer.get_best_score() <= 21:
                if dealer.get_best_score() < player.get_best_score():
                    print("Player won!")

                elif dealer.get_best_score() > player.get_best_score():
                    print("Dealer won!")

                else:
                    print("Tie!")

            else:
                print("The dealer bust!")

            print("Player score: %s" % player.get_best_score())
            print("Dealer score: %s" % dealer.get_best_score())

            correct_input = False

        elif player_status == 'h':
            player.receive_card(bj.cards[num_of_total_dealt_cards])
            num_of_total_dealt_cards += 1
            print("Player: %s" % player.print_hand())

            if player.get_best_score() < 21:
                player_status = input("Type 'h' to hit and 's' to stay:\n")

            elif player.get_best_score() == 21:
                player_status = 's'

            else:
                print('The player bust!')
                print("Player score: %s" % player.get_best_score())
                print("Dealer score: %s" % dealer.get_best_score())

                correct_input = False

        else:
            correct_input = False
            keep_playing = False

    play_again = input("Do you want to play again? [y/n]\n")
    if play_again != 'y':
        keep_playing = False

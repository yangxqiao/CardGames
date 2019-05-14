import unittest
from _card_games.blackjack import Card, CardCollection, make_deck, \
    BlackJackPlayer, is_yes_or_no, Robot, Human, BlackJackGame, \
    generate_robot_players

SUITS = ['hearts', 'spades', 'diamonds', 'clubs']
RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']


class TestCard(unittest.TestCase):

    def test_good_card_suit_no_exceptions(self):
        for suit in SUITS:
            Card(suit, '10')

    def test_bad_card_suit_raise_exceptions(self):
        for bad_suits in ['21', 'hi', None, True, 1, []]:
            self.assertRaises(ValueError, Card, bad_suits, '8', False)

    def test_good_card_rank_no_exceptions(self):
        for rank in RANKS:
            Card('hearts', rank)

    def test_bad_card_rank_with_exception(self):
        for bad_ranks in ['22' 'hi', None, True, 21, []]:
            self.assertRaises(ValueError, Card, 'hearts', bad_ranks, True)

    def test_good_is_face_up(self):
        for is_face_up in [True, False]:
            Card('hearts', '9', is_face_up)

    def test_bad_is_face_up(self):
        for is_face_up in ['22' 'hi', None, 21, []]:
            self.assertRaises(ValueError, Card, 'hearts', '9', is_face_up)

    def test_flip_card(self):

        is_face_up = True
        card1 = Card('hearts', '8', is_face_up)
        card2 = Card('hearts', '9', not is_face_up)

        self.assertTrue(card1.is_face_up)
        self.assertFalse(card2.is_face_up)

        card1.flip()
        card2.flip()

        self.assertFalse(card1.is_face_up)
        self.assertTrue(card2.is_face_up)


class TestCardCollection(unittest.TestCase):

    def test_valid_input_add_card(self):
        deck = CardCollection()
        card1 = Card('hearts', '10')
        card2 = Card('spades', '9')

        deck._add_card(card1)
        self.assertEqual(deck.cards, [card1])
        deck._add_card(card2)
        self.assertEqual(deck.cards, [card1, card2])

    def test_invalid_input_add_card(self):
        deck = CardCollection()
        card1 = 5
        card2 = 'ABC'
        card3 = ['hearts', 10]
        card4 = ['hearts', '10']

        for card in [card1, card2, card3, card4, None, []]:
            self.assertRaises(TypeError, deck._add_card, card)

    def test_valid_input_add_cards(self):
        deck = CardCollection()
        card1 = Card('hearts', '10')
        card2 = Card('spades', '9')
        card3 = Card('clubs', 'K')
        card4 = Card('diamonds', 'A')

        deck.add_cards(card1, card2, card3, card4)

    def test_invalid_input_add_cards(self):
        deck = CardCollection()
        card1 = Card('hearts', '10')
        card2 = Card('spades', '9')
        card3 = Card('clubs', 'K')

        deck.add_cards(card1, card2)
        self.assertEqual(deck.num_of_cards(), 2)

        deck.add_cards(*[card3] * 100)
        self.assertEqual(deck.num_of_cards(), 102)

    def test_pop_card_nonempty(self):
        deck = CardCollection()
        card1 = Card('hearts', '10')
        card2 = Card('spades', '9')

        deck.add_cards(card1)
        self.assertEqual(deck.cards, [card1])
        deck.pop_card()
        self.assertEqual(deck.cards, [])

        deck.add_cards(card1, card2)
        self.assertEqual(deck.cards, [card1, card2])
        deck.pop_card()
        self.assertEqual(deck.cards, [card1])
        deck.pop_card()
        self.assertEqual(deck.cards, [])

    def test_pop_card_empty(self):
        deck = CardCollection()
        self.assertRaises(IndexError, CardCollection.pop_card, deck)

    def test_flip_card(self):
        deck = CardCollection()
        make_deck(deck)

        for num in [-1, '2', 56, [100], None, []]:
            self.assertRaises(IndexError, deck.flip_card, num)

    def test_shuffle_change_order(self):
        deck = CardCollection()
        make_deck(deck)
        prev_cards = deck.cards.copy()

        deck.shuffle()
        self.assertNotEqual(deck.cards, prev_cards)

    def test_clear_clean_list(self):
        deck = CardCollection()
        make_deck(deck)

        deck.clear()
        self.assertEqual(deck.cards, [])


class TestBlackJackPlayer(unittest.TestCase):

    def test_valid_player_name_no_exception(self):
        for name in ['123', 'yan123', 'ABC', '[A]', 'None']:
            BlackJackPlayer(name)

    def test_invalid_player_name_raise_exception(self):
        for name in [[], None, 23]:
            self.assertRaises(ValueError, BlackJackPlayer, name)

    def test_points_property(self):
        card1 = Card('hearts', 'A')
        card2 = Card('spades', 'K')
        card3 = Card('clubs', '2')

        player1 = BlackJackPlayer('Yang')
        player1.hand.add_cards(*[card1] * 22)
        self.assertEqual(player1.points, 22)

        player2 = BlackJackPlayer('Yang')
        player2.hand.add_cards(*[card2] * 2, card1)
        self.assertEqual(player2.points, 21)

        player3 = BlackJackPlayer('Yang')
        make_deck(player3.hand)
        self.assertEqual(player3.points, 340)

        player4 = BlackJackPlayer('Yang')
        player4.hand.add_cards(card2, card3)
        self.assertEqual(player4.points, 12)

    def test_is_choose_to_hit(self):
        yang = BlackJackPlayer('Yang')
        self.assertRaises(NotImplementedError, yang.is_choose_to_hit)


class TestYesOrNo(unittest.TestCase):

    def test_valid_is_yes_or_no(self):
        for text in ['yes', 'YES']:
            self.assertEqual(is_yes_or_no(text), True)

        for text in ['no', 'NO']:
            self.assertEqual(is_yes_or_no(text), False)

    def test_invalid_is_yes_or_no(self):
        for text in [1, 2, 3, [], None]:
            self.assertRaises(TypeError, is_yes_or_no, text)

        for text in ['Definitely!', 'lol yes', 'No no no']:
            self.assertRaises(ValueError, is_yes_or_no, text)


class TestRobot(unittest.TestCase):

    def test_is_choose_to_hit(self):
        cards = []

        for i in range(13):
            cards.append(Card('hearts', RANKS[i]))

        # test points from 2 to 11
        for card in cards:
            robot = Robot('K7')
            robot.hand.add_cards(card)
            self.assertEqual(robot.is_choose_to_hit(), True)

        # test points from 12 to 16
        for card in cards[:5]:
            robot = Robot('K7')
            robot.hand.add_cards(card, cards[8])
            self.assertEqual(robot.is_choose_to_hit(), True)

        # test points from 17 to 21
        for card in cards[5:]:
            robot = Robot('K7')
            robot.hand.add_cards(card, cards[8])
            self.assertEqual(robot.is_choose_to_hit(), False)


class TestBlackJackGame(unittest.TestCase):

    def test_valid_dealer_player_input(self):
        dealer1 = Robot('J2')
        robot_players = generate_robot_players(20)
        BlackJackGame(dealer1, robot_players)

    def test_invalid_dealer_input(self):
        dealers = generate_robot_players(5)
        robot_players = generate_robot_players(2)
        self.assertRaises(TypeError, BlackJackGame, dealers, robot_players)

    def test_invalid_player_input(self):
        dealer1 = Robot('J2')
        player1 = Robot('K2')
        player2 = Robot('G3')

        self.assertRaises(TypeError, BlackJackGame, dealer1, player1, player2)

    def test_valid_output_num_of_players(self):
        pass


if __name__ == '__main__':
    unittest.main()

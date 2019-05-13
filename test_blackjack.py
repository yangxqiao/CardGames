import unittest
import random
from _card_games.blackjack import Card, CardCollection, make_deck

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

        for card in [card1, card2]:
            deck._add_card(card)

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
        # card1 = Card('hearts', '10')
        # card2 = Card('spades', '9')
        # card3 = Card('clubs', 'K')
        # card4 = Card('diamonds', 'A')
        #
        # self.assertRaises(TypeError, CardCollection.add_cards,
        #                   [card1, card2, card3, card4])
        #
        # self.assertRaises(TypeError, CardCollection.add_cards,
        #                   {card1: card2, card3: card4})
        pass

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

    def shuffle_change_order(self):
        deck = CardCollection()
        make_deck(deck)
        prev_cards = deck.cards

        for _ in range(10):
            deck.shuffle()
        self.assertNotEqual(deck.cards, prev_cards)


if __name__ == '__main__':
    unittest.main()

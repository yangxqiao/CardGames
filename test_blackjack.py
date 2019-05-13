import unittest

from _card_games.blackjack import Card

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

    """
    test_valid_input_add_card
    test_invalid_input_add_card
    test_valid_input_add_cards
    test_invalid_input_add_cards
    test_pop_card_nonempty
    test_shuffle_change_order

    """


if __name__ == '__main__':
    unittest.main()


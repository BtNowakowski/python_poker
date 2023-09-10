import pytest
from source.poker import Poker
from source.card import Card


class TestPoker:
    @pytest.fixture(autouse=True, scope="function")
    def poker(tmp_path):
        # Setup: fill with any logic you want
        poker = Poker()

        yield poker  # this is where the testing happens

        # Teardown : fill with any logic you want
        del poker

    def test_deal(self, poker):
        CARDS_TO_DEAL = 2

        len_deck = len(poker.cards)
        poker.shuffle_deck()
        player_cards = poker.deal(CARDS_TO_DEAL)
        assert (
            len(player_cards) == CARDS_TO_DEAL
            and len(poker.cards) + CARDS_TO_DEAL == len_deck
        )

    def test_deal_table(self, poker):
        CARDS_TO_DEAL = 5

        len_deck = len(poker.cards)
        poker.shuffle_deck()
        table_cards = poker.deal_table(CARDS_TO_DEAL)
        assert (
            len(table_cards) == CARDS_TO_DEAL
            and len(poker.cards) + CARDS_TO_DEAL == len_deck
        )

    def test_calculate_hand(self, poker):
        player_cards = [Card("Spade", "A"), Card("Spade", "A")]
        table_cards = [
            Card("Spade", "1"),
            Card("Spade", "2"),
            Card("Spade", "3"),
            Card("Spade", "4"),
            Card("Spade", "5"),
        ]
        hand, points, best_card = poker.calculate_hand(player_cards + table_cards)
        assert (
            hand == "Pair"
            and points == 2
            and best_card[0].index == "A"
            and best_card[1].shape == "Spade"
        )

    def test_valid_place_bet(self, poker):
        poker.player_money = 1000
        poker.computer_money = 1000
        poker.table_money = 0
        poker.place_bet(100)
        assert poker.player_money == 900 and poker.table_money == 100
        poker.computer_bet(100)
        assert poker.computer_money == 900 and poker.table_money == 200

    def test_invalid_place_bet(self, poker):
        poker.player_money = 1000
        poker.computer_money = 50
        poker.table_money = 0
        poker.place_bet(100)
        assert poker.place_bet(100) is False

    def test_valid_computer_bet(self, poker):
        poker.player_money = 1000
        poker.computer_money = 1000
        poker.table_money = 0
        poker.computer_bet(100)
        assert poker.computer_money == 900 and poker.table_money == 100

    def test_invalid_computer_bet(self, poker):
        poker.player_money = 50
        poker.computer_money = 1000
        poker.table_money = 0
        poker.computer_bet(100)
        assert poker.computer_bet(100) is False

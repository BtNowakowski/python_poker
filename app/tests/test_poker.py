import pytest
from source.poker import Poker
from source.player import Player
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
        player_cards = poker.deal(CARDS_TO_DEAL)
        assert (
            len(player_cards) == CARDS_TO_DEAL
            and len(poker.cards) + CARDS_TO_DEAL == len_deck
        )

    def test_deal_table(self, poker):
        CARDS_TO_DEAL = 5

        len_deck = len(poker.cards)
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
            and points == poker.points_dict["Pair"]
            and best_card[0].index == "A"
            and best_card[1].shape == "Spade"
        )

    def test_did_player_win__true(self, poker):
        player = Player(poker)
        computer = Player(poker)
        player.cards = [Card("Spade", "A"), Card("Spade", "A")]
        computer.cards = [Card("Spade", "K"), Card("Spade", "K")]
        player_initial_money = player.money
        computer_initial_money = computer.money

        BET_AMOUNT = 100
        table_cards = [
            Card("Spade", "1"),
            Card("Spade", "2"),
            Card("Spade", "3"),
            Card("Spade", "4"),
            Card("Spade", "A"),
        ]
        player.place_bet(BET_AMOUNT)
        computer.place_bet(BET_AMOUNT)

        assert (
            poker.did_player_win(player, computer, table_cards)[0] == True
            and computer.money == computer_initial_money - BET_AMOUNT
            and player.money == player_initial_money + BET_AMOUNT
        )

    def test_did_player_win__false(self, poker):
        player = Player(poker)
        computer = Player(poker)
        player.cards = [Card("Spade", "A"), Card("Spade", "A")]
        computer.cards = [Card("Spade", "K"), Card("Spade", "K")]
        player_initial_money = player.money
        computer_initial_money = computer.money

        BET_AMOUNT = 100
        table_cards = [
            Card("Spade", "1"),
            Card("Spade", "2"),
            Card("Spade", "3"),
            Card("Spade", "4"),
            Card("Spade", "K"),
        ]

        player.place_bet(BET_AMOUNT)
        computer.place_bet(BET_AMOUNT)

        assert (
            poker.did_player_win(player, computer, table_cards)[0] == False
            and computer.money == computer_initial_money + BET_AMOUNT
            and player.money == player_initial_money - BET_AMOUNT
        )

    def test_did_player_win__player_passed_no_bet(self, poker):
        player = Player(poker)
        computer = Player(poker)

        player.cards = [Card("Spade", "A"), Card("Spade", "A")]
        computer.cards = [Card("Spade", "K"), Card("Spade", "K")]

        computer_initial_money = computer.money

        BET_AMOUNT = 100

        table_cards = [
            Card("Spade", "1"),
            Card("Spade", "2"),
            Card("Spade", "3"),
            Card("Spade", "4"),
            Card("Spade", "A"),
        ]

        player.pass_q()

        computer.place_bet(BET_AMOUNT)

        assert (
            poker.did_player_win(player, computer, table_cards)[0] == False
            and computer.money == computer_initial_money
        )

    def test_did_player_win__player_passed_with_bet(self, poker):
        player = Player(poker)
        computer = Player(poker)

        player.cards = [Card("Spade", "A"), Card("Spade", "A")]
        computer.cards = [Card("Spade", "K"), Card("Spade", "K")]

        player_initial_money = player.money
        computer_initial_money = computer.money

        BET_AMOUNT = 100

        table_cards = [
            Card("Spade", "1"),
            Card("Spade", "2"),
            Card("Spade", "3"),
            Card("Spade", "4"),
            Card("Spade", "A"),
        ]
        player.place_bet(BET_AMOUNT)
        computer.place_bet(BET_AMOUNT)
        player.pass_q()

        assert (
            poker.did_player_win(player, computer, table_cards)[0] == True
            and player.money == player_initial_money + BET_AMOUNT
            and computer.money == computer_initial_money - BET_AMOUNT
        )

    def test_did_player_win__player_folded(self, poker):
        player = Player(poker)
        computer = Player(poker)

        player.cards = [Card("Spade", "A"), Card("Spade", "A")]
        computer.cards = [Card("Spade", "K"), Card("Spade", "K")]

        player_initial_money = player.money
        computer_initial_money = computer.money

        BET_AMOUNT = 100

        table_cards = [
            Card("Spade", "1"),
            Card("Spade", "2"),
            Card("Spade", "3"),
            Card("Spade", "4"),
            Card("Spade", "A"),
        ]
        player.place_bet(BET_AMOUNT)

        computer.place_bet(BET_AMOUNT)

        player.fold()

        assert (
            poker.did_player_win(player, computer, table_cards)[0] == False
            and player.money == player_initial_money - BET_AMOUNT
            and computer.money == computer_initial_money + BET_AMOUNT
        )

import pytest
from source.computer import Computer
from source.poker import Poker


class TestComputer:
    @pytest.fixture(autouse=True, scope="function")
    def objects(tmp_path):
        # Setup: fill with any logic you want

        poker = Poker()
        computer = Computer(poker)
        yield computer, poker  # this is where the testing happens

        # Teardown : fill with any logic you want
        del computer, poker

    def test_make_decision(self, objects):
        computer, poker = objects
        poker.table_money = 200
        computer_initial_money = computer.money
        table_initial_money = poker.table_money
        PLAYER_BET = 200
        computer.make_decision(PLAYER_BET, False, False)
        assert (table_initial_money + PLAYER_BET <= poker.table_money and computer_initial_money > computer.money)

    def test_make_decision__all_in(self, objects):
        computer, poker = objects
        poker.table_money = 1100
        table_initial_money = poker.table_money
        computer_initial_money = computer.money
        PLAYER_BET = 1100
        computer.make_decision(PLAYER_BET, False, True)
        assert (
            computer.money == 0
            and computer.all_in == True
            and poker.table_money == table_initial_money + computer_initial_money
        )

    def test_make_decision__player_all_in(self, objects):
        computer, poker = objects
        compter_initial_money = computer.money
        table_initial_money = poker.table_money
        PLAYER_BET = 100
        computer.make_decision(PLAYER_BET, False, True)
        assert (
            computer.money == compter_initial_money - PLAYER_BET
            and poker.table_money == table_initial_money + PLAYER_BET
        )
from source.player import Player
from source.poker import Poker
import pytest


class TestPlayer:
    @pytest.fixture(autouse=True, scope="function")
    def objects(tmp_path):
        # Setup: fill with any logic you want

        poker = Poker()
        player = Player(poker)
        yield player, poker  # this is where the testing happens

        # Teardown : fill with any logic you want
        del player

    def test_place_bet_valid(self, objects):
        player, poker = objects
        player.money = 1000
        player.place_bet(100)
        assert player.money == 900 and poker.table_money == 100

    def test_place_bet_invalid(self, objects):
        player, poker = objects
        player.money = 1000
        bet_placed = player.place_bet(1100)
        assert (
            bet_placed is not None and player.money == 1000 and poker.table_money == 0
        )

    def test_fold(self, objects):
        player, poker = objects
        player.fold()
        assert player.folded and player.cards == []

    def test_pass(self, objects):
        player, poker = objects
        player.pass_q()
        assert player.passed

    def test_reset(self, objects):
        player, poker = objects
        player.reset()
        assert not player.folded and not player.passed

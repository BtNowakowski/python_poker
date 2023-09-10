import pytest
from source.card import Card


class TestCard:
    def test_value(self):
        card = Card("Spade", "A")
        card1 = Card("Spade", "1")
        card2 = Card("Spade", "T")
        card3 = Card("Spade", "Q")

        assert card.value == 14
        assert card1.value == 1
        assert card2.value == 10
        assert card3.value == 12

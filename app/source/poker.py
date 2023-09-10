from random import shuffle as random_shuffle
from source.card import Card
from collections import Counter


class Poker:
    def __init__(self):
        self.cards = [
            [i, s]
            for i in "23456789TJQKA"
            for s in ["Spade", "Heart", "Diamond", "Club"]
        ]
        self.player_money = 1000
        self.computer_money = 1000
        self.points_dict = {
            "Royal Flush": 10,
            "Straight Flush": 9,
            "Four of a Kind": 8,
            "Full House": 7,
            "Flush": 6,
            "Straight": 5,
            "Three of a Kind": 4,
            "Two Pair": 3,
            "Pair": 2,
            "High Card": 1,
        }
        self.table_money = 0

    def shuffle_deck(self) -> None:
        random_shuffle(self.cards)

    def deal(self, number_of_cards: int = 2) -> list[Card]:
        deck = self.cards[:number_of_cards]
        del self.cards[:number_of_cards]
        return [Card(card[1], card[0]) for card in deck]

    def deal_table(self, number_of_cards: int = 5) -> list[Card]:
        deck = self.cards[:number_of_cards]
        del self.cards[:number_of_cards]
        return [Card(card[1], card[0]) for card in deck]

    def calculate_hand(self, hand: list[Card]) -> tuple[str, int, list[Card]]:
        indexes = [card.index for card in hand]
        values = [card.value for card in hand]

        counter = Counter(values)
        most_common_values = counter.most_common()

        unique_values = list(set(values))

        flush = len(set(indexes)) == 1

        straight = unique_values == 5 and max(unique_values) - min(unique_values) == 4

        royal_flush = straight and flush and min(unique_values) == 10

        best_cards = lambda x: [card for card in hand if card.value == x]

        if royal_flush:
            return ("Royal Flush", self.points_dict["Royal Flush"], best_cards(14))
        elif straight and flush:
            return (
                "Straight Flush",
                self.points_dict["Straight Flush"],
                best_cards(max(unique_values)),
            )
        elif most_common_values[0][1] == 4:
            return (
                "Four of a Kind",
                self.points_dict["Four of a Kind"],
                best_cards(most_common_values[0][0]),
            )
        elif most_common_values[0][1] == 3 and most_common_values[1][1] == 2:
            return (
                "Full House",
                self.points_dict["Full House"],
                best_cards(most_common_values[0][0])
                + best_cards(most_common_values[1][0]),
            )
        elif flush:
            return ("Flush", self.points_dict["Flush"], best_cards(max(unique_values)))
        elif straight:
            return (
                "Straight",
                self.points_dict["Straight"],
                best_cards(max(unique_values)),
            )
        elif most_common_values[0][1] == 3:
            return (
                "Three of a Kind",
                self.points_dict["Three of a Kind"],
                best_cards(most_common_values[0][0]),
            )
        elif most_common_values[0][1] == 2 and most_common_values[1][1] == 2:
            return (
                "Two Pair",
                self.points_dict["Two Pair"],
                best_cards(most_common_values[0][0])
                + best_cards(most_common_values[1][0]),
            )
        elif most_common_values[0][1] == 2:
            return (
                "Pair",
                self.points_dict["Pair"],
                best_cards(most_common_values[0][0]),
            )
        else:
            return (
                "High Card",
                self.points_dict["High Card"],
                best_cards(max(unique_values)),
            )

    def place_bet(self, amount: int) -> int | bool:
        if amount > self.player_money:
            # raise ValueError("You don't have enough money")
            return False
        if amount > self.computer_money:
            # raise ValueError("The computer doesn't have enough money")
            return False
        self.player_money -= amount
        self.table_money += amount
        return amount

    def computer_bet(self, amount: int) -> int | bool:
        if amount > self.computer_money:
            # raise ValueError("The computer doesn't have enough money")
            return False
        if amount > self.player_money:
            # raise ValueError("Player doesn't have enough money")
            return False
        self.computer_money -= amount
        self.table_money += amount
        return amount

    def main_loop(self):
        self.shuffle_deck()
        while True:
            player_cards = self.deal()
            computer_cards = self.deal()
            table_cards = self.deal_table()

            bet = self.place_bet(100)
            computer_bet = self.computer_bet(100)

            player_hand, player_points, player_best_card = self.calculate_hand(
                player_cards + table_cards
            )
            computer_hand, computer_points, computer_best_card = self.calculate_hand(
                computer_cards + table_cards
            )
            if player_points > computer_points or (
                player_points == computer_points
                and player_best_card[0].value > computer_best_card[0].value
            ):
                print(f"Player wins! {player_hand}")
                self.player_money += self.table_money
                self.table_money = 0
            elif player_points < computer_points or (
                computer_points == player_points
                and computer_best_card[0].value > player_best_card[0].value
            ):
                print(f"Computer wins! {computer_hand}")
                self.computer_money += self.table_money
                self.table_money = 0
            else:
                print(f"Draw! - Both players had {player_hand}")
                self.player_money += bet
                self.computer_money += computer_bet
                self.table_money = 0
            break

        print("Player cards:")
        for card in player_cards:
            print(card.shape, card.index)
        print()
        print("Computer cards:")
        for card in computer_cards:
            print(card.shape, card.index)
        print()
        print("Table cards:")
        for card in table_cards:
            print(card.shape, card.index)
        print()

        print(
            f"Player Points: {player_points}, Hand: {player_hand}, Best Card: {player_best_card[0].index} {player_best_card[0].shape}"
        )

        print(
            f"Computer Points: {computer_points}, Hand: {computer_hand}, Best Card: {computer_best_card[0].index} {computer_best_card[0].shape}"
        )

        print()
        print(self.player_money)
        print(self.computer_money)
        print(self.table_money)

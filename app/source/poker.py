from random import shuffle as random_shuffle
import time
from source.console_interface import ConsoleInterface
from source.card import Card
from source.player import Player
from collections import Counter


class Poker:
    def __init__(self):
        self.cards = [
            [i, s]
            for i in "23456789TJQKA"
            for s in ["Spade", "Heart", "Diamond", "Club"]
        ]
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
        self.shuffle_deck()
        deck = self.cards[:number_of_cards]
        del self.cards[:number_of_cards]
        return [Card(card[1], card[0]) for card in deck]

    def deal_table(self, number_of_cards: int = 3) -> list[Card]:
        self.shuffle_deck()
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

    def clear_table(self, *players: Player) -> None:
        self.cards = [
            [i, s]
            for i in "23456789TJQKA"
            for s in ["Spade", "Heart", "Diamond", "Club"]
        ]
        self.table_money = 0
        for player in players:
            player.cards = []
            player.current_bet = 0

    def main_loop(self):
        player = Player(self)
        computer = Player(self)
        interface = ConsoleInterface()
        while True:
            if player.money <= 0:
                print("You lost all your money!")
                break
            elif computer.money <= 0:
                print("You won all the money!")
                break
            player.cards = self.deal()
            computer.cards = self.deal()
            table_cards = self.deal_table()
            while len(table_cards) <= 5:
                self.shuffle_deck()
                interface.clear()
                player.reset()
                print("Table cards: ", end="")
                interface.show_cards(table_cards)

                print("\nYour cards: ", end="")
                interface.show_cards(player.cards)

                print(f"\nYour money: {player.money}")
                print(f"\nTable money: {self.table_money}")

                print(f"Player bet: {player.current_bet}")
                print(f"Computer bet: {computer.current_bet}")

                continue_playing = interface.ask_continue()

                if continue_playing is not None and not continue_playing:
                    player.fold()
                    break
                elif continue_playing is None:
                    player.pass_q()
                    print("You passed!")

                if not player.passed:
                    bet = interface.ask_bet()
                    player.place_bet(bet)

                    computer.place_bet(100)

                table_cards += self.deal_table(1)

            if (
                not player.folded
                and not computer.folded
                and not (player.passed and self.table_money == 0)
            ):
                player_hand, player_points, player_best_card = self.calculate_hand(
                    player.cards + table_cards
                )
                (
                    computer_hand,
                    computer_points,
                    computer_best_card,
                ) = self.calculate_hand(computer.cards + table_cards)

                if player_points > computer_points or (
                    player_points == computer_points
                    and player_best_card[0].value > computer_best_card[0].value
                ):
                    print(f"Player wins! {player_hand}")
                    player.money += self.table_money
                    time.sleep(2)
                elif player_points < computer_points or (
                    computer_points == player_points
                    and computer_best_card[0].value > player_best_card[0].value
                ):
                    print(f"Computer wins! {computer_hand}")
                    computer.money += self.table_money
                    time.sleep(2)
                else:
                    print(f"Draw! - Both players had {player_hand}")
                    player.money += player.current_bet
                    computer.money += computer.current_bet
                    time.sleep(2)
            elif computer.folded:
                print("Computer folded!")
                player.money += self.table_money
            elif player.folded:
                print("Player folded!")
                computer.money += self.table_money
            else:
                print("Both players passed!")
            self.clear_table(player, computer)

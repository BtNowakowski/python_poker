import os


class ConsoleInterface:
    def clear(self):
        if os.name == "nt":
            os.system("cls")
        else:
            os.system("clear")

    def ask_bet(self, player_bet, computer_bet):
        int_bet = 0
        # written in a way to allow player bet at the game start when players bets are equal
        while computer_bet > player_bet or computer_bet == player_bet:
            try:
                int_bet = int(input("\nPlace your bet: "))
                player_bet += int_bet
                # we dont want to make player bet more than computer, he might like to put the same amount
                if computer_bet == player_bet:
                    break
            except ValueError:
                print("Invalid input!")
            except KeyboardInterrupt:
                print("Exiting...")
                exit(0)
        return int_bet

    def show_cards(self, cards):
        for card in cards:
            print(card.index + " - " + card.shape, end=", ")

    def ask_continue(self):
        while True:
            try:
                u_continue = input("\nBet, fold or pass? (B/F/P): ").upper()

                if u_continue == "B":
                    return True
                elif u_continue == "F":
                    return False
                elif u_continue == "P":
                    return None
                else:
                    print("Invalid input!")
                    continue
            except ValueError:
                print("Invalid input!")
                continue
            except KeyboardInterrupt:
                print("Exiting...")
                exit(0)

    def ask_bet_fold(self):
        while True:
            try:
                u_continue = input("\nBet or fold? (B/F): ").upper()

                if u_continue == "B":
                    return True
                elif u_continue == "F":
                    return False
                else:
                    print("Invalid input!")
                    continue
            except ValueError:
                print("Invalid input!")
                continue
            except KeyboardInterrupt:
                print("Exiting...")
                exit(0)

    def display_all_info(self, player, computer, table_money, table_cards):
        print("Table cards: ", end="")
        self.show_cards(table_cards)

        print("\nYour cards: ", end="")
        self.show_cards(player.cards)

        print(f"\nYour money: {player.money}")
        print(f"\nTable money: {table_money}")

        if player.passed:
            print(f"Player bet: {player.current_bet} - passed!")
        elif player.folded:
            print("You folded!")
        elif player.all_in:
            print(f"Player bet: {player.current_bet} - all in!")
        else:
            print(f"Player bet: {player.current_bet}")

        if computer.passed:
            print(f"Computer bet: {computer.current_bet} - passed!")
        elif computer.folded:
            print("Computer folded!")
        elif computer.all_in:
            print(f"Computer bet: {computer.current_bet} - all in!")
        else:
            print(f"Computer bet: {computer.current_bet}")

    def show_winner(self, did_player_win, hand):
        if did_player_win is None:
            if hand == "Pass":
                print("\nDraw! Both players passed!")
            else:
                print(f"\nDraw! Both players had {hand}")
        elif did_player_win:
            if hand == "Fold":
                print("\nPlayer wins! Computer folded!")
            else:
                print(f"\nPlayer wins! You had {hand}")
        else:
            if hand == "Fold":
                print("\nComputer wins! Player folded!")
            else:
                print(f"\nComputer wins! It had {hand}")

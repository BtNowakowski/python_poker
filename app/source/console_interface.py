import os


class ConsoleInterface:
    def clear(self):
        if os.name == "nt":
            os.system("cls")
        else:
            os.system("clear")

    def ask_bet(self):
        try:
            int_bet = int(input("\nPlace your bet: "))
            return int_bet
        except ValueError:
            print("Invalid input!")
            self.ask_bet()
        except KeyboardInterrupt:
            print("Exiting...")
            exit(0)

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

class Player:
    def __init__(self, poker_game, money=1000):
        self.money = money
        self.cards = []
        self.game = poker_game
        self.current_bet = 0
        self.folded = False
        self.passed = False
        self.all_in = False

    def place_bet(self, bet) -> bool | None:
        if bet > self.money:
            return False
        self.money -= bet
        self.current_bet += bet
        self.game.table_money += bet

        if self.money == 0:
            self.all_in = True

    def fold(self):
        self.folded = True
        self.cards = []

    def pass_q(self):
        self.passed = True

    def reset(self):
        self.folded = False
        self.passed = False

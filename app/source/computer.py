from source.player import Player
from random import choice as random_choice


class Computer(Player):
    def __init__(self, poker_game, money=1000):
        super().__init__(poker_game, money)
        self.possible_bets = [0, 100, 200, 300, 400, 500]

    def make_decision(self, player_bet, is_player_passing, is_player_all_in):
        if is_player_all_in:
            if player_bet > self.current_bet and self.money >= player_bet:
                self.place_bet(player_bet)
            elif player_bet < self.current_bet:
                self.pass_q()
            else:
                self.place_bet(self.money)
                self.all_in = True
        elif player_bet > self.current_bet and self.money >= player_bet:
            self.place_bet(player_bet)
        elif self.money <= player_bet and self.money > 0:
            self.place_bet(self.money)
            self.all_in = True
        elif self.money == 0:
            self.pass_q()
        elif player_bet < self.current_bet:
            self.pass_q()
        elif is_player_passing or player_bet == self.current_bet:
            random_bet = self.money + 1
            while random_bet > self.money:
                random_bet = random_choice(self.possible_bets)
            if random_bet == 0:
                self.pass_q()
            else:
                self.place_bet(random_bet)

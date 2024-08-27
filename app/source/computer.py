from source.player import Player
from random import choice as random_choice


class Computer(Player):
    def __init__(self, poker_game, money=1000):
        super().__init__(poker_game, money)
        self.possible_bets = [0, 100, 200, 300, 400, 500]
        self.possible_raise = [0, 0, 0, 50, 100, 200]

    def make_decision(self, player_bet, is_player_passing, is_player_all_in):
        player_bet_now = player_bet - self.current_bet
        if is_player_all_in:
            if player_bet > self.current_bet and self.money >= player_bet:
                self.place_bet(player_bet)
            elif player_bet < self.current_bet or (
                player_bet == self.current_bet and self.current_bet != 0
            ):
                self.pass_q()
            else:
                self.place_bet(self.money)
                self.all_in = True
        elif player_bet > self.current_bet and self.money >= player_bet_now:
            self.place_bet(player_bet_now + random_choice(self.possible_raise))
        elif self.money <= player_bet_now and self.money > 0:
            self.place_bet(self.money)
            self.all_in = True
        elif self.money == 0:
            self.pass_q()
        elif player_bet < self.current_bet:
            self.pass_q()
        elif is_player_passing or player_bet == self.current_bet:
            while True: 
                random_bet = random_choice(self.possible_bets)
                if random_bet <= self.money: break
            if random_bet == 0:
                self.pass_q()
            else:
                self.place_bet(random_bet)

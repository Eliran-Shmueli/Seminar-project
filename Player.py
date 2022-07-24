import socket

def plus_one(variable):
    return variable + 1


class Player:
    def __init__(self, player_id, player_name):
        self.id = player_id
        self.name = player_name
        self.socket = None
        self.num_games = 0
        self.num_wins = 0
        self.num_losses = 0
        self.num_ties = 0
        self.num_rock = 0
        self.num_paper = 0
        self.num_scissors = 0

    def get_name(self):
        return self.name

    def get_id(self):
        return self.id

    def increase_num_games(self):
        self.num_games = plus_one(self.num_games)

    def increase_num_wins(self):
        self.num_wins = plus_one(self.num_wins)

    def increase_num_losses(self):
        self.num_losses = plus_one(self.num_losses)

    def increase_num_ties(self):
        self.num_ties = plus_one(self.num_ties)

    def increase_num_rock(self):
        self.num_rock = plus_one(self.num_rock)

    def increase_num_paper(self):
        self.num_paper = plus_one(self.num_paper)

    def increase_num_scissors(self):
        self.num_scissors = plus_one(self.num_scissors)

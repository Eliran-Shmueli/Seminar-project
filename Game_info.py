from Player import Player

def plus_one(variable):
    return variable + 1

class Game_info:
    def __init__(self, player_id, player_name):
        self.player_info = Player(player_id, player_name)
        self.num_games=0
        self.num_rounds=0
        self.num_wins = 0
        self.num_losses = 0
        self.num_ties = 0
        self.num_rock = 0
        self.num_paper = 0
        self.num_scissors = 0

    def increase_num_games(self):
        self.num_games = plus_one(self.num_games)

    def increase_num_rounds(self):
        self.num_rounds = plus_one(self.num_games)

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

    def get_player_id(self):
        return self.player_info.get_id()

    def get_player_name(self):
        return self.player_info.get_name()

    def create_copy(self):
        temp_game_info = Game_info(self.get_player_id(),self.get_player_name())
        temp_game_info.num_games = self.num_games
        temp_game_info.num_rounds = self.num_rounds
        temp_game_info.num_wins = self.num_wins
        temp_game_info.num_losses = self.num_losses
        temp_game_info.num_ties = self.num_ties
        temp_game_info.num_rock = self.num_rock
        temp_game_info.num_paper = self.num_paper
        temp_game_info.num_scissors = self.num_scissors
        return temp_game_info

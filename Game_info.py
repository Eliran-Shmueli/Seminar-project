from Player import Player

def plus_one(variable):
    return variable + 1

class Game_info:
    def __init__(self, player_id, player_name):
        """
        init Game_info
        :param player_id: player id
        :param player_name: player name
        """
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
        """
        increase number of games played
        """
        self.num_games = plus_one(self.num_games)

    def increase_num_rounds(self):
        """
        increase number of rounds played in a game
        """
        self.num_rounds = plus_one(self.num_rounds)

    def increase_num_wins(self):
        """
        increase number of wins
        """
        self.num_wins = plus_one(self.num_wins)

    def increase_num_losses(self):
        """
        increase number of losses
        """
        self.num_losses = plus_one(self.num_losses)

    def increase_num_ties(self):
        """
        increase number of ties
        """
        self.num_ties = plus_one(self.num_ties)

    def increase_num_rock(self):
        """
        increase number of times player selected rock
        """
        self.num_rock = plus_one(self.num_rock)

    def increase_num_paper(self):
        """
        increase number of times player selected paper
        """
        self.num_paper = plus_one(self.num_paper)

    def increase_num_scissors(self):
        """
        increase number of times player selected scissors
        """
        self.num_scissors = plus_one(self.num_scissors)

    def get_player_id(self):
        """
        returns player's id
        """
        return self.player_info.get_id()

    def get_player_name(self):
        """
        returns player's name
        """
        return self.player_info.get_name()

    def create_copy(self):
        """
        returns copy of the game information
        """
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

def plus_one(variable):
    return variable + 1


class PlayerInfo:
    tags = {'id': "Player's id", 'name': "Player's name", 'num_games': 'Number of games',
            'num_wins': 'Number of wins',
            'num_losses': 'Number of losses', 'num_ties': 'Number of ties', 'num_rock': 'Selected rock',
            'num_paper': 'Selected paper', 'num_scissors': 'Selected Scissors'}

    def __init__(self, player_id, player_name):
        """
        init Player_info
        :param player_id: player id
        :param player_name: player name
        """
        self.id = player_id
        self.name = player_name
        self.num_games = 0
        self.num_wins = 0
        self.num_losses = 0
        self.num_ties = 0
        self.num_rock = 0
        self.num_paper = 0
        self.num_scissors = 0

        self.List_games = []

    def get_name(self):
        """
        get player's name
        :return: name
        """
        return self.name

    def get_id(self):
        """
        get player's id
        :return: id
        """
        return self.id

    def increase_num_games(self):
        """
        increase number of games played
        """
        self.num_games = plus_one(self.num_games)

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

    def update_info(self, player_info, game_info):
        """
        updates player information and adds new game info to list
        :param player_info: new player info
        :param game_info: new game info
        """
        self.List_games.append(game_info)  # adds game info to list
        self.num_games = self.num_games + player_info.num_games
        self.num_wins = self.num_wins + player_info.num_wins
        self.num_losses = self.num_losses + player_info.num_losses
        self.num_ties = self.num_ties + player_info.num_ties
        self.num_rock = self.num_rock + player_info.num_rock
        self.num_paper = self.num_paper + player_info.num_paper
        self.num_scissors = self.num_scissors + player_info.num_scissors

    def clear_results(self):
        """
        set all results to 0
        """
        self.num_games = 0
        self.num_wins = 0
        self.num_losses = 0
        self.num_ties = 0
        self.num_rock = 0
        self.num_paper = 0
        self.num_scissors = 0

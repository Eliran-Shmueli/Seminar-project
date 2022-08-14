
class Player:
    def __init__(self, player_id, player_name):
        """
        inti Player
        :param player_id: player id
        :param player_name: player name
        """
        self.id = player_id
        self.name = player_name
        self.socket = None

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

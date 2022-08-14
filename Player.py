from PlayerInfo import PlayerInfo


class Player:
    def __init__(self, player_id, player_name):
        """
        init Player
        :param player_id: player id
        :param player_name: player name
        """
        self.socket = None
        self.id = player_id
        self.name = player_name

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

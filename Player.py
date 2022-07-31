


class Player:
    def __init__(self, player_id, player_name):
        self.id = player_id
        self.name = player_name
        self.socket = None

    def get_name(self):
        return self.name

    def get_id(self):
        return self.id



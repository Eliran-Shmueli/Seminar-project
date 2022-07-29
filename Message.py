class Message:
    def __init__(self, id_client):
        self.dict_messages = {0: "connected", 1: "ready", 2: "choose", 3: "exit", 4: "goodbye", 5: "data"}
        self.id = id_client
        self.message = None
        self.num_data = 0
        self.data = None

    def set_message_connected(self):
        self.message = self.dict_messages[0]

    def set_message_ready(self):
        self.message = self.dict_messages[1]

    def set_message_choose(self):
        self.message = self.dict_messages[2]

    def set_message_exit(self):
        self.message = self.dict_messages[3]

    def set_message_goodbye(self):
        self.message = self.dict_messages[4]

    def add_data_to_message(self, data):
        self.data = data
        if data is None:
            self.num_data = 0
        else:
            self.num_data = 1

    def is_message_connected(self):
        if self.message == self.dict_messages[0]:
            return True
        else:
            return False

    def is_message_ready(self):
        if self.message == self.dict_messages[1]:
            return True
        else:
            return False

    def is_message_choose(self):
        if self.message == self.dict_messages[2]:
            return True
        else:
            return False

    def is_message_exit(self):
        if self.message == self.dict_messages[3]:
            return True
        else:
            return False

    def is_message_goodbye(self):
        if self.message == self.dict_messages[4]:
            return True
        else:
            return False

    def is_message_data(self):
        if self.num_data == 1:
            return True
        else:
            return False

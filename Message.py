class Message:
    def __init__(self, client_id):
        """
        init Message
        :param client_id: the id of a client
        """
        self.dict_messages = {0: "join request", 1: "accepted", 2: "choose", 3: "exit", 4: "goodbye", 5: "game info "
                                                                                                         "request"}
        self.id = client_id
        self.message = None
        self.num_data = 0
        self.data = None

    def set_message_join_request(self):
        """
        set message to "join request"
        """
        self.message = self.dict_messages[0]

    def set_message_accepted(self):
        """
        set message to "accepted"
        """
        self.message = self.dict_messages[1]

    def set_message_choose(self):
        """
        set message to "choose"
        """
        self.message = self.dict_messages[2]

    def set_message_exit(self):
        """
        set message to "exit"
        """
        self.message = self.dict_messages[3]

    def set_message_goodbye(self):
        """
        set message to "goodbye"
        """
        self.message = self.dict_messages[4]

    def set_message_game_info_request(self):
        """
        set message to "game info request"
        """
        self.message = self.dict_messages[5]

    def add_data_to_message(self, data):
        """
        adds data to message
        :param data: data object to send
        """
        self.data = data
        if data is None:
            self.num_data = 0
        else:
            self.num_data = 1

    def is_message_join_request(self):
        """
        returns true if message is "join request",if not returns false
        :return: boolean
        """
        if self.message == self.dict_messages[0]:
            return True
        else:
            return False

    def is_message_accepted(self):
        """
        returns true if message is "accepted",if not returns false
        :return: boolean
        """
        if self.message == self.dict_messages[1]:
            return True
        else:
            return False

    def is_message_choose(self):
        """
        returns true if message is "choose",if not returns false
        :return: boolean
        """
        if self.message == self.dict_messages[2]:
            return True
        else:
            return False

    def is_message_exit(self):
        """
        returns true if message is "exit",if not returns false
        :return: boolean
        """
        if self.message == self.dict_messages[3]:
            return True
        else:
            return False

    def is_message_goodbye(self):
        """
        returns true if message is "goodbye",if not returns false
        :return: boolean
        """
        if self.message == self.dict_messages[4]:
            return True
        else:
            return False

    def is_message_game_info_request(self):
        """
        returns true if message is "game info request",if not returns false
        :return: boolean
        """
        if self.message == self.dict_messages[5]:
            return True
        else:
            return False

    def is_message_have_data(self):
        """
        returns true if message has data,if not returns false
        :return: boolean
        """
        if self.num_data == 1:
            return True
        else:
            return False

import socket
import selectors
import types
import pickle
import random
from Message import Message


class Server:
    HEADERSIZE = 10

    def __init__(self, Q_messages_send, Q_messages_received, dic_players, event):
        """
        init server
        :param Q_messages_send: queue of messages to send
        :param Q_messages_received: queue of messages server received
        :param dic_players: dictionary of players
        :param event: an Event to stop the server
        """
        self.Q_messages_received = Q_messages_received
        self.Q_messages_send = Q_messages_send
        self.sel = selectors.DefaultSelector()
        self.host = socket.gethostname()
        self.port = 1231
        self.full_msg = b''
        self.dic_players = dic_players
        self.message = Message(0)
        self.event_stop = event

    def run(self):
        """
        server init socket and listing on it for incoming and outgoing data.
        if there are messages on Q_messages_send, sends all.
        """
        lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        lsock.bind((self.host, self.port))
        lsock.listen()
        self.log_message(f"Listening on {(self.host, self.port)}")
        lsock.setblocking(False)
        self.sel.register(lsock, selectors.EVENT_READ, data=None)

        try:
            while not self.event_stop.is_set():
                while self.Q_messages_send.empty() is False:
                    key, message = self.Q_messages_send.get()
                    self.append_message(key.data, message)
                events = self.sel.select(timeout=1)
                for key, mask in events:
                    if key.data is None:
                        self.accept_wrapper(key.fileobj)
                    else:
                        self.service_connection(key, mask)
        finally:
            self.sel.close()

    def accept_wrapper(self, sock):
        """
        creates new socket for new client and adds to selector
        :param sock: socket of the server
        """
        socket_connected, addr = sock.accept()  # Should be ready to read
        socket_connected.setblocking(False)
        data = types.SimpleNamespace(addr=addr, byte_in=b"", byte_out=b"")
        events = selectors.EVENT_READ | selectors.EVENT_WRITE
        self.sel.register(socket_connected, events, data=data)
        self.log_message(f"Accepted connection from {addr}")

    def service_connection(self, key, mask):
        """
        send message or receive accordingly to the mask
        :param key: socket
        :param mask: send or receive message
        """
        sock = key.fileobj
        data = key.data
        if mask & selectors.EVENT_READ:
            recv_data = sock.recv(1024)  # Should be ready to read
            if recv_data:
                data.byte_in += recv_data
                message_received = pickle.loads(data.byte_in[self.HEADERSIZE:])
                self.log_message("Info from client " + str(message_received.id) + ": " + message_received.message)
                self.actions(message_received, key)
                data.byte_in = b''
        if mask & selectors.EVENT_WRITE:
            if data.byte_out:
                sent = sock.send(data.byte_out)  # Should be ready to write
                data.byte_out = data.byte_out[sent:]
                data.byte_out = b''

    def actions(self, message_received, key):
        """
        actions to do according to the received message
        :param message_received: received message
        :param key: socket
        """
        if message_received.is_message_goodbye():
            self.log_message("client id " + str(message_received.id) + " has exit")
            self.log_message(f"Closing connection to {key.data.addr}")
            self.close_client_connection(message_received, key)
        elif message_received.is_message_game_results() or message_received.is_message_exit():
            self.Q_messages_received.put((key, message_received))
        else:
            if message_received.is_message_join_request():
                player_id = message_received.id
                self.dic_players[player_id].socket = key
                self.message.set_message_accepted()
            if message_received.is_message_choose():
                self.message.set_message_choose()
                self.message.add_data_to_message(self.computer_pick(message_received.id))
            self.append_message(key.data, self.message)

    def append_message(self, data, message):
        """
        convert message to bytes and adds it to data.byte_out
        :param data: data of a socket
        :param message: message to send
        """
        data.byte_out = pickle.dumps(message)
        data.byte_out = bytes(f"{len(data.byte_out):<{self.HEADERSIZE}}", 'utf-8') + data.byte_out

    def close_client_connection(self, message_received, key):
        """
        close connection with client and remove him from dictionary
        :param message_received: massage from client
        :param key: socket
        """
        del self.dic_players[message_received.id]
        self.sel.unregister(key.fileobj)
        key.fileobj.close()

    def log_message(self, logs):
        """
        sends to main thread info to log
        :param logs: str
        """
        log = Message(0)
        log.set_message_log_info()
        log.add_data_to_message(logs)
        self.Q_messages_received.put((None, log))

    def computer_pick(self, id):
        """
        generate random option for the computer
        :return: "rock"|"paper"|"scissors"
        """
        choice = random.choice(["rock", "paper", "scissors"])
        self.log_message("Selected " + choice + ", sends to client " + str(id))
        return choice

import socket
import selectors
import types
import pickle
import logging
import random
from Message import Message


def computer_pick():
    """
    generate random option for the computer
    :return: "rock"|"paper"|"scissors"
    """
    choice = random.choice(["rock", "paper", "scissors"])
    logging.info('Pc chose - ' + choice)
    return choice


class Server:
    HEADERSIZE = 10

    def __init__(self, Q_messages_send, Q_messages_received, dic_players, event):
        """
        init server
        :param Q_messages_send: queue of messages to send
        :param Q_messages_received: queue of messages sever received
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
        self.message = Message(-1)
        self.event_stop = event

    def run(self):
        """
        server init socket and listing on it for incoming and outgoing data.
        if there are messages on Q_messages_send, sends all.
        """
        lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        lsock.bind((self.host, self.port))
        lsock.listen()
        print(f"sever - Listening on {(self.host, self.port)}")
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
        except KeyboardInterrupt:
            print("sever - Caught keyboard interrupt, exiting")
        finally:
            self.sel.close()

    def accept_wrapper(self, sock):
        """
        creates new socket for new client and adds to selector
        :param sock: socket of the server
        """
        socket_connected, addr = sock.accept()  # Should be ready to read
        print(f"server - Accepted connection from {addr}")
        socket_connected.setblocking(False)
        data = types.SimpleNamespace(addr=addr, byte_in=b"", byte_out=b"")
        events = selectors.EVENT_READ | selectors.EVENT_WRITE
        self.sel.register(socket_connected, events, data=data)

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
                print("sever - info from client " + message_received.message)
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
            print("client id " + str(message_received.id) + " has exit")
            print(f"sever - Closing connection to {key.data.addr}")
            del self.dic_players[message_received.id]
            self.sel.unregister(key.fileobj)
            key.fileobj.close()
        elif message_received.is_message_game_info_request() or message_received.is_message_exit():
            self.Q_messages_received.put((key, message_received))
        else:
            if message_received.is_message_join_request():
                player_id = message_received.id
                self.dic_players[player_id].socket = key
                self.message.set_message_accepted()
            if message_received.is_message_choose():
                self.message.set_message_choose()
                self.message.add_data_to_message(computer_pick())
            self.append_message(key.data, self.message)

    def append_message(self, data, message):
        """
        convert message to bytes and adds it to data.byte_out
        :param data: data of a socket
        :param message: message to send
        """
        data.byte_out = pickle.dumps(message)
        data.byte_out = bytes(f"{len(data.byte_out):<{self.HEADERSIZE}}", 'utf-8') + data.byte_out

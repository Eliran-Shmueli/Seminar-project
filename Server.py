import socket
import selectors
import types
import pickle
import logging
import random
from Message import Message


def computer_pick():
    """generate random option for the computer"""
    choice = random.choice(["rock", "paper", "scissors"])
    logging.info('Pc chose - ' + choice)
    return choice


class Server:
    HEADERSIZE = 10

    def __init__(self, Q_messages_send, Q_messages_received, dic_players,event):
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
        # finally:
        # self.sel.close()

    def accept_wrapper(self, sock):
        socket_connected, addr = sock.accept()  # Should be ready to read
        print(f"server - Accepted connection from {addr}")
        socket_connected.setblocking(False)
        data = types.SimpleNamespace(addr=addr, byte_in=b"", byte_out=b"")
        events = selectors.EVENT_READ | selectors.EVENT_WRITE
        self.sel.register(socket_connected, events, data=data)

    def service_connection(self, key, mask):
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

        # else:
        # print(f"sever - Closing connection to {data.addr}")
        # self.sel.unregister(sock)
        # sock.close()
        if mask & selectors.EVENT_WRITE:

            if data.byte_out:
                sent = sock.send(data.byte_out)  # Should be ready to write
                data.byte_out = data.byte_out[sent:]
                data.byte_out = b''

    def actions(self, message_received, key):
        if message_received.is_message_goodbye():
            print("client id " + str(message_received.id) + " has exit")
            print(f"sever - Closing connection to {key.data.addr}")
            self.sel.unregister(key.fileobj)
            key.fileobj.close()

        elif message_received.is_message_connect_to_server():
            self.Q_messages_received.put((key, message_received))
        else:
            if message_received.is_message_connected():
                player_id = message_received.id
                self.dic_players[player_id].socket = key
                self.message.set_message_ready()
            if message_received.is_message_choose():
                self.message.set_message_choose()
                self.message.add_data_to_message(computer_pick())
            if message_received.is_message_exit():
                self.message.set_message_goodbye()
                self.Q_messages_received.put((key,message_received))
            self.append_message(key.data, self.message)

    def append_message(self, data, message):
        data.byte_out = pickle.dumps(message)
        data.byte_out = bytes(f"{len(data.byte_out):<{self.HEADERSIZE}}", 'utf-8') + data.byte_out

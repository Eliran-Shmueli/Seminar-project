import socket
import selectors
import types
import pickle
import logging
import random
import queue

def computer_pick():
    """generate random option for the computer"""
    choice = random.choice(["rock", "paper", "scissors"])
    logging.info('Pc chose - ' + choice)
    return choice


class Server:
    HEADERSIZE = 10

    def __init__(self,queue):
        self.Q_server=queue
        self.sel = selectors.DefaultSelector()
        self.host = socket.gethostname()
        self.port = 1231
        self.full_msg = b''
        self.dict_clients = {}
        self.dict_messages = {0: "id", 1: "ready",  2: "choose",3:"exit",4:"bye"}

    def run(self):
        lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        lsock.bind((self.host, self.port))
        lsock.listen()
        print(f"sever - Listening on {(self.host, self.port)}")
        lsock.setblocking(False)
        self.sel.register(lsock, selectors.EVENT_READ, data=None)

        try:
            while True:
                events = self.sel.select(timeout=None)
                for key, mask in events:
                    if key.data is None:
                        self.accept_wrapper(key.fileobj)
                    else:
                        self.service_connection(key, mask)
        except KeyboardInterrupt:
            print("sever - Caught keyboard interrupt, exiting")
        #finally:
           # self.sel.close()

    def accept_wrapper(self, sock):
        socket_connected, addr = sock.accept()  # Should be ready to read
        print(f"sever - Accepted connection from {addr}")
        socket_connected.setblocking(False)
        data = types.SimpleNamespace(addr=addr, inb=b"", outb=b"")
        events = selectors.EVENT_READ | selectors.EVENT_WRITE
        self.sel.register(socket_connected, events, data=data)

    def service_connection(self, key, mask):
        sock = key.fileobj
        data = key.data
        if mask & selectors.EVENT_READ:
            recv_data = sock.recv(1024)  # Should be ready to read
            if recv_data:
                data.inb += recv_data
                data_received = pickle.loads(data.inb[self.HEADERSIZE:])
                print("sever - info from client " + data_received)
                self.actions(data_received, key, mask)
                data.inb=b''

           # else:
               # print(f"sever - Closing connection to {data.addr}")
               # self.sel.unregister(sock)
               # sock.close()
        if mask & selectors.EVENT_WRITE:

            if data.outb:
                sent = sock.send(data.outb)  # Should be ready to write
                data.outb = data.outb[sent:]
                data.outb = b''

    def actions(self, data_received, key, mask):
        if data_received[0:2] == self.dict_messages[0]: # id
           # id = data_received[3:]
            # self.dict_clients[id] = (key, mask)
            self.append_message(key.data,self.dict_messages[1])
        if data_received==self.dict_messages[2]: # choose
            self.append_message(key.data,computer_pick())
        if data_received[0:4] == self.dict_messages[3]:  # exit
            self.append_message(key.data, self.dict_messages[4])
            self.Q_server.put(data_received)


    def append_message(self, data, message):
        data.outb = pickle.dumps(message)
        data.outb = bytes(f"{len(data.outb):<{self.HEADERSIZE}}", 'utf-8') + data.outb

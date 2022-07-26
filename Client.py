import sys
import socket
import selectors
import types
import pickle
import queue


class Client:
    HEADERSIZE = 10

    def __init__(self, player_info):
        host = socket.gethostname()
        port = 1231
        self.dict_messages = {0: "id", 1: "ready", 2: "choose",3:"exit",4:"bye"}
        self.Q_messages_received = queue.Queue()
        self.Q_messages_send =queue.Queue()
        self.Q_messages_send.put(self.dict_messages[0] + " " + str(player_info.id))
        self.sel = selectors.DefaultSelector()
        self.player_info = player_info

        self.run = True
        self.output_send = None
        self.start_connections(host, port)

    def run_cl(self):
        try:
            while self.run:
                events = self.sel.select(timeout=1)
                if events:
                    for key, mask in events:
                        self.service_connection(key, mask)
                # Check for a socket being monitored to continue.
                if not self.sel.get_map():
                    break
        except KeyboardInterrupt:
            print("client id " + str(self.player_info.id) + "  - Caught keyboard interrupt, exiting")

    # finally:
    #    self.sel.close()

    def start_connections(self, host, port):
        server_addr = (host, port)

        print(f"client id " + str(self.player_info.id) + " - Starting connection - player id " + str(
            self.player_info.id) + " to " + str(server_addr))
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setblocking(False)
        sock.connect_ex(server_addr)
        events = selectors.EVENT_READ | selectors.EVENT_WRITE
        data = types.SimpleNamespace(inb=b"", outb=b"")
        self.sel.register(sock, events, data=data)

    def service_connection(self, key, mask):
        sock = key.fileobj
        HEADERSIZE = 10
        data = key.data
        if mask & selectors.EVENT_READ:
            recv_data = sock.recv(1024)  # Should be ready to read
            if recv_data:
                data.inb += recv_data
                data_received = pickle.loads(data.inb[self.HEADERSIZE:])
                self.Q_messages_received.put(data_received)
                print("client id " + str(self.player_info.id) + " - info from server: " + data_received)
                data.inb=b""
                self.run = False
        #  if not recv_data:
        # print(f"Closing connection ")
        # self.sel.unregister(sock)
        #  sock.close()
        if mask & selectors.EVENT_WRITE:

            if not data.outb and self.Q_messages_send.empty() is False:
                data.outb = pickle.dumps(self.Q_messages_send.get())
                data.outb = bytes(f"{len(data.outb):<{HEADERSIZE}}", 'utf-8') + data.outb
                if data.outb:
                    sent = sock.send(data.outb)  # Should be ready to write
                    data.outb = data.outb[sent:]
                    # self.run = True

    def send_info(self, data):
        self.run = True
        self.Q_messages_send.put(data)
        self.run_cl()

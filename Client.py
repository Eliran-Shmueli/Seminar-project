import sys
import socket
import selectors
import types
import pickle
import queue


class Client:
    HEADERSIZE = 10

    def __init__(self, player_info,queue):
        host = socket.gethostname()
        port = 1231
        self.dict_messages = {0: "id", 1: "ready", 2: "start"}
        self.queue=queue
        self.sel = selectors.DefaultSelector()
        self.player_info = player_info
        self.messages = [self.dict_messages[0]+" "+str(player_info.id)]
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
            print("Caught keyboard interrupt, exiting")

    # finally:
    #    self.sel.close()

    def start_connections(self, host, port):
        server_addr = (host, port)

        print(f"Starting connection - player id " + str(self.player_info.id) + " to " + str(server_addr))
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
                self.queue.put(data_received)
                print("info from server "+str(self.player_info.id)+ " " + data_received)
                self.run=False
          #  if not recv_data:
               # print(f"Closing connection ")
               # self.sel.unregister(sock)
              #  sock.close()
        if mask & selectors.EVENT_WRITE:

            if not data.outb and self.messages:

                data.outb = pickle.dumps(self.messages.pop(0))
                data.outb = bytes(f"{len(data.outb):<{HEADERSIZE}}", 'utf-8') + data.outb
                if data.outb:
                    sent = sock.send(data.outb)  # Should be ready to write
                    data.outb = data.outb[sent:]
                    #self.run = True

    def send_info(self, data):
        self.run = True
        self.messages.append(data)
        self.run_cl()

import socket
import selectors
import types
import pickle


class Client:
    HEADERSIZE = 10

    def __init__(self, player_id, Q_messages_send, Q_messages_received, event):
        host = socket.gethostname()
        port = 1231
        self.player_id = player_id
        self.Q_messages_received = Q_messages_received
        self.Q_messages_send = Q_messages_send
        self.sel = selectors.DefaultSelector()
        self.event_stop = event
        self.output_send = None
        self.start_connections(host, port)
        self.run_cl()

    def run_cl(self):
        try:
            while not self.event_stop.is_set():
                events = self.sel.select(timeout=1)
                if events:
                    for key, mask in events:
                        self.service_connection(key, mask)
                # Check for a socket being monitored to continue.
                if not self.sel.get_map():
                    break
        except OSError:
            print("client id " + str(self.player_id) + " - Server is not connected")

    # finally:
    #    self.sel.close()

    def start_connections(self, host, port):
        server_addr = (host, port)

        print(f"client id " + str(self.player_id) + " - Starting connection - player id " + str(
            self.player_id) + " to " + str(server_addr))
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setblocking(False)
        sock.connect_ex(server_addr)
        events = selectors.EVENT_READ | selectors.EVENT_WRITE
        data = types.SimpleNamespace(byte_in=b"", byte_out=b"")
        self.sel.register(sock, events, data=data)

    def service_connection(self, key, mask):
        sock = key.fileobj
        HEADERSIZE = 10
        data = key.data
        if mask & selectors.EVENT_READ:
            recv_data = sock.recv(1024)  # Should be ready to read
            if recv_data:
                data.byte_in += recv_data
                message_received = pickle.loads(data.byte_in[self.HEADERSIZE:])
                self.Q_messages_received.put(message_received)
                print("client id " + str(self.player_id) + " - info from server: " + message_received.message)
                if message_received.is_message_data():
                    print("server chose - " + message_received.data)
                data.byte_in = b""

        if mask & selectors.EVENT_WRITE:

            if not data.byte_out and self.Q_messages_send.empty() is False:
                data.byte_out = pickle.dumps(self.Q_messages_send.get())
                data.byte_out = bytes(f"{len(data.byte_out):<{HEADERSIZE}}", 'utf-8') + data.byte_out
                if data.byte_out:
                    sent = sock.send(data.byte_out)  # Should be ready to write
                    data.byte_out = data.byte_out[sent:]


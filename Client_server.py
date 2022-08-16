import socket
import selectors
import types
import pickle

from Message import Message


class Client:
    HEADERSIZE = 10

    def __init__(self, player_id, Q_messages_send, Q_messages_received, event):
        """
        init client server
        :param player_id: the id of the player
        :param Q_messages_send: queue of messages to send
        :param Q_messages_received: queue of messages that the client server received
        :param event: a stop event, in order to stop the server on demand
        """
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

    def start_connections(self, host, port):
        """
        starts connection to server
        :param host: server ip address
        :param port: port number
        """
        server_addr = (host, port)

        self.log_message(f"Starting connection - player id " + str(self.player_id) + " to " + str(server_addr))
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setblocking(False)
        sock.connect_ex(server_addr)
        events = selectors.EVENT_READ | selectors.EVENT_WRITE
        data = types.SimpleNamespace(byte_in=b"", byte_out=b"")
        self.sel.register(sock, events, data=data)

    def run_cl(self):
        """
        runs client server, checking for input or output events until receiving stop event
        """
        try:
            while not self.event_stop.is_set():
                events = self.sel.select(timeout=1)
                if events:
                    for key, mask in events:
                        self.service_connection(key, mask)
                # Check for a socket being monitored to continue.
                if not self.sel.get_map():
                    break
        finally:
            self.sel.close()

    def service_connection(self, key, mask):
        """
        receive and send data to server accordingly
        :param key: socket
        :param mask: events - sending or receiving
        """
        sock = key.fileobj
        HEADERSIZE = 10
        data = key.data
        if mask & selectors.EVENT_READ:
            recv_data = sock.recv(1024)  # Should be ready to read
            if recv_data:
                data.byte_in += recv_data
                message_received = pickle.loads(data.byte_in[self.HEADERSIZE:])
                self.Q_messages_received.put(message_received)
                self.log_message("Info from server: " + message_received.message)
                data.byte_in = b""

        if mask & selectors.EVENT_WRITE:
            if not data.byte_out and self.Q_messages_send.empty() is False:
                data.byte_out = pickle.dumps(self.Q_messages_send.get())
                data.byte_out = bytes(f"{len(data.byte_out):<{HEADERSIZE}}", 'utf-8') + data.byte_out
                if data.byte_out:
                    sent = sock.send(data.byte_out)  # Should be ready to write
                    data.byte_out = data.byte_out[sent:]

    def log_message(self, logs):
        """
        sends to main thread info to log
        :param logs: str
        """
        log = Message(-1)
        log.set_message_log_info()
        log.add_data_to_message(logs)
        self.Q_messages_received.put(log)

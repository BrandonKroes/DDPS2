import pickle
import socket


class ReceiveSocket:
    stack = []

    def __init__(self, args):
        # Pipe is mandatory
        self.port = None
        self.host = None
        pipe, margs = args
        self.socket = socket.socket()
        self.pipe = pipe
        for k, v in margs.items():
            self.__dict__[k] = v

        self.setup_socket()
        self.main()

    def setup_socket(self):
        self.socket.bind((self.host, self.port))

    def main(self):
        with self.socket as s:
            s.listen()
            conn, addr = s.accept()
            buffer = ""

            with conn:
                print(f"Connected by {addr}")
                while True:
                    data = conn.recv(1024)
                    if not data:
                        self.pipe.send(pickle.loads(buffer))
                        break
                    buffer = buffer + data
                conn.close()

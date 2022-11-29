from common.communication.endpoint_config import EndpointConfig
import socket
import pickle

import multiprocessing
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
        # TODO: Let the OS pick a port: https://stackoverflow.com/questions/1365265/on-localhost-how-do-i-pick-a-free-port-number
        self.socket.bind((self.host, self.port))
        self.socket.listen(1)

    def get_message(self, conn, addr, pipe):
        with conn:
            buffer = b''
            print(f"Connected by {addr}")
            is_data = True
            while is_data:
                data = conn.recv(10000)
                if not data:
                    is_data = False
                buffer = buffer + data
            pipe.send(pickle.loads(buffer))
            conn.close()

    def main(self):
        while True:
            conn, address = self.socket.accept()
            process = multiprocessing.Process(
                target=self.get_message(conn, address, self.pipe), args=(conn, address, self.pipe))
            process.daemon = True
            process.start()


class SendSocket:
    stack = []

    def __init__(self, pipe, **kwargs):
        # Pipe is mandatory
        self.pipe = pipe
        for k, v in kwargs.items():
            self.__dict__[k] = v
        self.main()

    def send_message(self, packet: EndpointConfig):
        s = socket.socket(packet.connection_type[0], packet.connection_type[1])
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.connect((packet.host, packet.port))
        s.sendall(pickle.dumps(packet), )
        s.close()

        return

    def main(self):
        while True:
            if self.pipe.poll():  # checking if we actually have to do something
                packet = self.pipe.recv()
                # if type(packet) == EndpointConfig.__class__:
                self.send_message(packet)
                # else:
                #    print("invalid message || " + str(packet) + " ||")

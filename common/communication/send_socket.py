import pickle
import socket

from common.communication import EndpointConfig


class SendSocket:
    stack = []

    def __init__(self, pipe, **kwargs):
        # Pipe is mandatory
        self.pipe = pipe
        for k, v in kwargs.items():
            self.__dict__[k] = v
        self.main()

    def send_message(self, packet: EndpointConfig):
        try:
            s = socket.socket(packet.connection_type[0], packet.connection_type[1])
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.connect((packet.host, packet.port))
            s.sendall(pickle.dumps(packet), )
            s.close()
        except ConnectionRefusedError:
            print("port error")
        return

    def main(self):
        while True:
            if self.pipe.poll():  # checking if we actually have to do something
                packet = self.pipe.recv()
                # TODO: check if type is actually the right type. if type(packet) == EndpointConfig.__class__:
                self.send_message(packet)
                # else:
                #    print("invalid message || " + str(packet) + " ||")

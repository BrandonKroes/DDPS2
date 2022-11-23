from common.communication.endpoint_config import EndpointConfig
import socket
import pickle


class SendSocket:
    stack = []

    def __init__(self, pipe, **kwargs):
        # Pipe is mandatory
        self.pipe = pipe
        for k, v in kwargs.items():
            self.__dict__[k] = v
        self.main()

    def send_message(self, packet: EndpointConfig):
        s = socket.socket(packet.connection_type)
        s.connect(packet.host, packet.port)
        s.sendall(pickle.dumps(packet.dataframe))
        return

    def main(self):
        while True:
            if self.pipe.poll():  # checking if we actually have to do something
                packet = self.pipe.recv()
                if type(packet) == EndpointConfig.__class__:
                    self.send_message(packet)
                else:
                    print("invalid message || " + str(packet) + " ||")

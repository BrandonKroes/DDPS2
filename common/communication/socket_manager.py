from common.communication import EndpointConfig


class SocketManager:
    send_sockets = []
    receive_sockets = []
    communication_log = []

    def __init__(self):
        pass

    def send_packet(self, message: EndpointConfig):
        pass

    def receive_queue(self):
        pass

    def write_to_log(self, record):
        pass

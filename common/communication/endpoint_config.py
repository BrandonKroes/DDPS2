# File that contains the schema for a send request
from common.communication.connection_type import ConnectionType
from common.packets.abstract_packet import AbstractPacket


class EndpointConfig:
    port = 0000
    host = "127.0.0.1"
    dataframe: AbstractPacket = None
    connection_type: ConnectionType = ""  # assuming TCP, but can be changed.

    def __init__(self, host, port, packet, connection_type=ConnectionType.TCP):
        self.port = port
        self.host = host
        self.packet = packet
        self.connection_type = connection_type
from socket import *


class Client:

    OUTGOING_PORT = 13000
    INCOMING_PORT = 13001
    BUFFER_SIZE = 1024

    def __init__(self, server_address):
        self.SERVER_ADDR = server_address
        self.outgoing, self.incoming = socket(
            AF_INET, SOCK_DGRAM), socket(AF_INET, SOCK_DGRAM)
        self.incoming.bind(("", self.INCOMING_PORT))
        self.buffer = ""

    def request(self, data=""):
        self.outgoing.sendto(self.encode(
            data), (self.SERVER_ADDR, self.OUTGOING_PORT))
        (data, addr) = self.incoming.recvfrom(self.BUFFER_SIZE, )
        self.buffer = self.decode(data)
    
    def close(self):
        self.outgoing.close()
        self.incoming.close()

    def encode(self, string):
        return bytes(string, 'utf-8')

    def decode(self, string):
        return string.decode("utf-8")
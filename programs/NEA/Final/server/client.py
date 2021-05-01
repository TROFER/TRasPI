from socket import *
import time
import json


class Client:

    OutgoingPort = 43334
    IncomingPort = 43333
    BufferSize = 1024

    def __init__(self):
        self.ServerAddr = "192.168.1.251"
        self.outgoing, self.incoming = socket(
            AF_INET, SOCK_DGRAM), socket(AF_INET, SOCK_DGRAM)
        self.incoming.bind(("", self.IncomingPort))
        self.buffer = ""

    def request(self, data="*"):
        self.outgoing.sendto(self.encode(
            data), (self.ServerAddr, self.OutgoingPort))
        (data, addr) = self.incoming.recvfrom(self.BufferSize, )
        print(self.decode(data))

    def close(self):
        self.outgoing.close()
        self.incoming.close()

    def encode(self, string):
        return bytes(string, 'utf-8')

    def decode(self, string):
        return json.loads(string.decode("utf-8"))


client = Client()
print("Client Initalised")
while True:
    client.request("gg")
    time.sleep(1)

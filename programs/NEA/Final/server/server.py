from socket import *
from app import App
import json

_inuse = False

class Server:

    IncomingPort = 43334
    OutgoingPort = 43333
    BufferSize = 1024

    def __init__(self, callback):
        global _inuse
        self._stop = False
        # Callback
        self.callback = callback
        # Socket Setup
        if not _inuse:
            self.incoming = socket(AF_INET, SOCK_DGRAM)
            self.outgoing = socket(AF_INET, SOCK_DGRAM)
            self.incoming.bind(("", self.IncomingPort))
            _inuse = True
        else:
            if App.const.debug:
                print(f"[DEBUG] - Server Already Active")
            raise OSError
    
    def await_requests(self):
        if App.const.debug:
            print(f"[DEBUG] - [Telemetry Server] Incoming: {self.IncomingPort} Outgoing: {self.OutgoingPort}")
        while not self._stop:
            try:
                (data, addr) = self.incoming.recvfrom(self.BufferSize)
                self.outgoing.sendto(self.encode(self.callback()), (addr[0], self.OutgoingPort))
            except BaseException as e:
                if App.const.debug:
                    print(f"[DEBUG] - Error Serving Request: {e}")
        
    def stop(self):
        global _inuse
        if App.const.debug:
            print(f"[DEBUG] - Stopping Server")
        self._stop = True
        self.outgoing.sendto(self.encode(""), ("localhost", self.IncomingPort)) # Forfils Hanging Condition
        self.incoming.close()
        _inuse = False
        

    def encode(self, string):
        string = json.dumps(string)
        return bytes(string, 'utf-8')


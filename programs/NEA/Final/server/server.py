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
            print(
                f"[DEBUG] - [Telemetry Server] Incoming: {self.IncomingPort} Outgoing: {self.OutgoingPort}")
        while not self._stop:
            try:
                (data, addr) = self.incoming.recvfrom(self.BufferSize)
                result = self.parameterize(self.decode(data))
                try:
                    self.outgoing.sendto(self.encode(
                        result), (addr[0], self.OutgoingPort))
                except BaseException as e:
                    if App.const.debug:
                        print(f"[DEBUG] - Error While Obtaining: {e}")
            except BaseException as e:
                if App.const.debug:
                    print(f"[DEBUG] - Error Serving Request: {e}")

    def stop(self):
        global _inuse
        if App.const.debug:
            print(f"[DEBUG] - Stopping Server")
        self._stop = True
        # Forfils Hanging Condition
        self.outgoing.sendto(self.encode(""), ("localhost", self.IncomingPort))
        self.incoming.close()
        _inuse = False

    def parameterize(self, request):
        if "*" in request:
            return self.callback()
        else:
            source = self.callback()
            result = {"errors": []}
            for field in request.replace(" ", "").split(","):
                print(field)
                try:
                    result[field] = source[field]
                except KeyError:
                    result["errors"].append(f"KeyError: {field}")
            if not result["errors"]:
                result.pop("errors")
            return result

    def encode(self, _dict):
        string = json.dumps(_dict)
        return bytes(string, 'utf-8')

    def decode(self, string):
        return string.decode("utf-8")

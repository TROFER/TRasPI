import subprocess
from ..error.attributes import SysConstant
from ..interface import Interface
from ..sys.proc import Process
from ..sys.net import Request

if SysConstant.pipeline == "GFXHAT":
    _FLAG = True
else:
    _FLAG = False

class Connection:
    def __init__(self, name: str, ip: str):
        self.name = name
        self.ip = ip

    def __bool__(self) -> bool:
        return self.ip is not None

    @property
    def ssid(self) -> str:
        return self.name

    def active(self) -> bool:
        return bool(self)

class Internet:
    def __init__(self, ip: str):
        self.ip = ip

    def __bool__(self) -> bool:
        return self.ip is not None

    def active(self) -> bool:
        return bool(self)

class Network:

    def __init__(self):
        self.__conn = Connection("NULL", None)
        self.__inet = Internet(None)

        if SysConstant.process:
            if SysConstant.platform == "NT":
                async def _get_local():
                    pass
            else: # UNIX
                async def _get_local():
                    pass
            async def check_for_connection():
                await _get_local()
                if self.__conn:
                    try:
                        self.__inet.ip = (await Request("https://ifconfig.me/ip")).read().decode()
                    except ConnectionError as e:
                        print(e)
                        self.__inet.ip = None

            self.__rescan = Interface.interval(check_for_connection, delay=30)

    @property
    def connection(self) -> Connection:
        return self.__conn
    @property
    def internet(self) -> Internet:
        return self.__inet

Network = Network()
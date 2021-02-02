import asyncio
import subprocess
from ..error.attributes import SysConstant
from ..interface import Interface
from ..sys.proc import Process
from ..sys.net import Request

# if SysConstant.pipeline == "GFXHAT":
#     _FLAG = True
# else:
#     _FLAG = False

class Connection:
    def __init__(self, event: asyncio.Event, name: str, ip: str):
        self.__event = asyncio.Event()
        self.name = name
        self.ip = ip

    def __bool__(self) -> bool:
        return self.__event.is_set()

    @property
    def ssid(self) -> str:
        """Interface Name"""
        return self.name

    def active(self) -> bool:
        """Current Connection Status"""
        return bool(self)

    def __await__(self):
        return self.wait().__await__()
    async def wait(self):
        """Wait for a Local Connection"""
        return await self.__event.wait()

class Internet:
    def __init__(self, event: asyncio.Event, ip: str):
        self.__event = event
        self.ip = ip

    def __bool__(self) -> bool:
        return self.__event.is_set()
        # return self.ip is not None

    def active(self) -> bool:
        """Current Connection Status"""
        return bool(self)

    def __await__(self):
        return self.wait().__await__()
    async def wait(self):
        """Wait for an Internet Connection"""
        return await self.__event.wait()

class Device:
    def __init__(self, hostname: str, name: str, mac: str):
        self.hostname = hostname
        self.name = name
        self.mac = mac

class Network:

    def __init__(self):
        self.__conn_event = asyncio.Event()
        self.__conn = Connection(self.__conn_event, "NULL", None)
        self.__inet_event = asyncio.Event()
        self.__inet = Internet(self.__inet_event, None)
        self.__dev = Device(None, None, None)

        if SysConstant.process:
            if SysConstant.platform == "NT":
                async def _setup():
                    self.__dev.hostname = (await Process("hostname", shell=True)).stdout.strip()
                async def _get_local():
                    cmd = """$a = Get-NetAdapter -Physical | ? Status -EQ "up" | Select-Object -Index 0;$addrs = Get-NetIPAddress -InterfaceIndex $a.InterfaceIndex;class Network {[string] $IPv4;[string] $IPv6;[string] $Mac;};$n = New-Object Network -Property @{"IPv4"=($addrs | Where-Object AddressFamily -Like ipv4).IPAddress;"IPv6"=($addrs | Where-Object AddressFamily -Like ipv6).IPAddress;"Mac"=$a.MacAddress;};$n.IPv4;$n.IPv6;$n.Mac;"""
                    self.__conn.ip, ipv6, self.__dev.mac = (await Process(cmd, shell=True)).stdout.split("\n")
            else: # UNIX
                async def _setup():
                    self.__dev.hostname = (await Process("hostname -I", shell=True)).stdout.strip()
                async def _get_local():
                    self.__dev.mac = "00:0a:95:9d:68:16"
            async def check_for_connection():
                await _get_local()
                if self.__conn:
                    try:
                        self.__inet.ip = (await Request("https://ifconfig.me/ip")).read().decode()
                    except ConnectionError as e:
                        print(e)
                        self.__inet.ip = None

            Interface.schedule(_setup())
            self.__rescan = Interface.interval(check_for_connection, delay=30)

    @property
    def connection(self) -> Connection:
        return self.__conn
    @property
    def internet(self) -> Internet:
        return self.__inet
    @property
    def device(self) -> Device:
        return self.__dev

Network = Network()

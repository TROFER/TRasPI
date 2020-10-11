import urllib.request
import http.client
from ..interface import Interface
from typing import Union

class Request:
    def __init__(self, url, **kwargs):
        self.__proc = Interface.process(urllib.request.urlopen, url, **kwargs)

    def __await__(self):
        return self.wait().__await__()

    async def wait(self) -> Union[http.client.HTTPResponse, urllib.request.URLopener]:
        return await self.__proc

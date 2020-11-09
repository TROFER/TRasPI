from ..error import logging as log
import traceback
import http.client
import urllib.request
from typing import Union
from ..interface import Interface

class Request:

    def __init__(self, url, **kwargs):
        self.__url = url
        self.__proc = Interface.process(urllib.request.urlopen, url, **kwargs)

    def __await__(self):
        return self.wait().__await__()

    async def wait(self) -> Union[http.client.HTTPResponse, urllib.request.URLopener]:
        try:
            return await self.__proc
        except Exception as e:
            log.program.warning("%s -> %s: %s", self.__class__.__qualname__, self.__url, type(e).__name__, e)
            log.traceback.warning("%s -> %s", self.__class__.__qualname__, self.__url, exc_info=e)
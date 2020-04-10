import asyncio
import concurrent
import threading

class AsyncController:

    def __init__(self):
        self._executor_cpu = concurrent.futures.ThreadPoolExecutor(thread_name_prefix="AsyncCPU")
        self._executor_io = concurrent.futures.ThreadPoolExecutor(thread_name_prefix="AsyncIO")

    async def main(self, application: "Application"):
        await application.main()

class Interface:

    def __init__(self, _async: AsyncController):
        self.__async = _async

    def run(self, application: "Application"):
        self.__application = application
        asyncio.run(self.__async.main(application))

    def application(self) -> "Application":
        return self.__application

    def render(self, obj: "Primative"):
        return self.__application.render.submit(obj)

Interface = Interface(AsyncController())
interface = Interface

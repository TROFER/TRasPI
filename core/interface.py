import asyncio
import concurrent
import threading

class AsyncController:

    def __init__(self):
        self._executor_cpu = concurrent.futures.ThreadPoolExecutor(thread_name_prefix="AsyncCPU")
        self._executor_io = concurrent.futures.ThreadPoolExecutor(thread_name_prefix="AsyncIO")

        self.loop = asyncio.new_event_loop()

    def run(self, application: "Application"):
        try:
            application.initialize()
            asyncio.run_coroutine_threadsafe(application.main(), self.loop)
            self.loop.run_forever()
        finally:
            self.loop.stop()
            application.terminate()
            self.loop.run_until_complete(self.loop.shutdown_asyncgens())
            self.loop.close()

    async def executor_cpu(self, func):
        return await self.loop.run_in_executor(self._executor_cpu, func)
    async def executor_cpu(self, func):
        return await self.loop.run_in_executor(self._executor_io, func)

class Interface:

    def __init__(self, _async: AsyncController):
        self.__async = _async

    def run(self, application: "Application"):
        self.__application = application
        self.__async.run(application)

    def active(self) -> bool:
        """Is the program actively running"""
        return self.__application.running

    def application(self) -> "Application":
        """Returns the Application"""
        return self.__application

    def render(self, obj: "Primative"):
        """Render Primative"""
        return self.__application.render.submit(obj)

    def schedule(self, coroutine):
        """Schedule Coroutine to Run"""
        asyncio.run_coroutine_threadsafe(coroutine, self.__async.loop)

    async def process(self, func, type: ("CPU", "IO")):
        """Process Intense Func on another Thread"""
        if type == "IO":
            return await self.__async.executor_io(func)
        return await self.__async.executor_cpu(func)

Interface = Interface(AsyncController())
interface = Interface

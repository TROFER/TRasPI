import asyncio
import concurrent
import threading
import core.error

class AsyncController:

    def __init__(self):
        self._executor_cpu = concurrent.futures.ThreadPoolExecutor(thread_name_prefix="AsyncCPU")
        self._executor_io = concurrent.futures.ThreadPoolExecutor(thread_name_prefix="AsyncIO")

        self.loop = asyncio.new_event_loop()

    def run(self, application: "Application"):
        try:
            application.initialize()
            asyncio.run_coroutine_threadsafe(application.run(), self.loop)
            self.loop.run_forever()
        finally:
            self.loop.stop()
            application.terminate()
            self.loop.run_until_complete(self.loop.shutdown_asyncgens())
            self.loop.close()

    async def executor_cpu(self, func):
        try:
            return await self.loop.run_in_executor(self._executor_cpu, func)
        except Exception as e:
            raise core.error.ExecutorProcessCPU(e) from e
    async def executor_cpu(self, func):
        try:
            return await self.loop.run_in_executor(self._executor_io, func)
        except Exception as e:
            raise core.error.ExecutorProcessIO(e) from e

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

    class interval:
        """Call func repeatedly, determinded by repeat, with a delay in seconds"""

        def __init__(self, func: callable, delay: float=1, repeat: int=-1):
            """Call func repeatedly, determinded by repeat, with a delay in seconds"""
            self._cancel = False
            self._event = asyncio.Event()
            self.func = func
            self.delay = delay
            self.repeat = repeat
            interface.schedule(self.run())

        def cancel(self):
            """Cancel the interval"""
            self._cancel = True

        def pause(self):
            self._event.clear()
        def resume(self):
            self._event.set()

        def __await__(self):
            return self.run().__await__()

        async def run(self):
            await asyncio.sleep(self.delay)
            while not self._cancel:
                await self._event.wait()
                try:
                    self.func()
                except Exception as e:
                    print(e)
                await asyncio.sleep(self.delay)

        def __hash__(self) -> int:
            return id(self)


Interface = Interface(AsyncController())
interface = Interface

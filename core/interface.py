import asyncio
import concurrent
import threading
import traceback
import functools
import core.error
import time
from .error import logging as log
from typing import Union, Coroutine, Callable, Any

class Batch:
    def __init__(self):
        self.__callbacks = set()

    def schedule(self, function: Union[Coroutine, Callable, asyncio.Future], *args: Any, **kwargs: Any) -> asyncio.Future:
        fut = Interface.loop.create_future()
        async def execute():
            try:
                if not fut.cancelled():
                    return fut.set_result(await Interface.schedule(function, *args, **kwargs))
                if asyncio.iscoroutine(function):
                    function.throw(asyncio.CancelledError)
            except Exception as e:
                fut.set_exception(e)
        self.__callbacks.add(execute())
        return fut

    async def finish(self):
        while self.__callbacks:
            callbacks = self.__callbacks.copy()
            await Interface.wait(*callbacks)
            self.__callbacks -= callbacks

class Interface:

    def __init__(self):
        self.__executor_io = concurrent.futures.ThreadPoolExecutor()
        self.__executor_cpu = concurrent.futures.ProcessPoolExecutor()
        self.__loop = asyncio.get_event_loop()
        self.__active = asyncio.Event()

        self.termintate = Batch()

    def __repr__(self):
        if self.single():
            return f"{self.__class__.__name__}"
        return f"{self.__class__.__name__}<{mp.current_process().name}>"

    @property
    def loop(self) -> asyncio.AbstractEventLoop:
        return self.__loop

    def active(self) -> bool:
        return not self.__active.is_set()

    def stop(self):
        if self.active():
            self.__active.set()
            self.__loop.call_soon_threadsafe(self.__loop.stop)

    def main(self, application: "Application"):
        self.__application = application
        self.__application.initialize()
        try:
            self.__active.clear()
            with self.__executor_cpu, self.__executor_io:
                self.schedule(self.__application.run())
                self.__loop.run_forever()
        finally:
            self.__active.set()
            self.__application.terminate()
            self.__loop.run_until_complete(self.__application.close_all())
            self.__loop.run_until_complete(self.termintate.finish())
            self.__loop.run_until_complete(self.next())
            self.__loop.run_until_complete(self.__loop.shutdown_asyncgens())
            self.__loop.stop()
            self.__loop.close()

    def schedule(self, function: Union[Coroutine, Callable, asyncio.Future], *args: Any, **kwargs: Any) -> asyncio.Future:
        if asyncio.iscoroutine(function): # Coroutine
            return asyncio.wrap_future(asyncio.run_coroutine_threadsafe(function, self.__loop), loop=self.__loop)
        elif asyncio.iscoroutinefunction(function): # Coroutine Function
            return self.schedule(function(*args, **kwargs))
        elif asyncio.isfuture(function): # Future
            return function
        elif callable(function): # Function
            fut = self.__loop.create_future()
            def execute():
                try:
                    if not fut.cancelled():
                        return fut.set_result(function(*args, **kwargs))
                except Exception as e:
                    fut.set_exception(e)
            self.__loop.call_soon_threadsafe(execute)
            return fut
        raise TypeError(f"'function' must be of type 'Coroutine', 'Callable', 'asyncio.Future' not '{function.__class__.__name__}'")

    async def process(self, func, *args, execute_type: str="io", **kwargs):
        exec_func = functools.partial(func, *args, **kwargs)
        if execute_type.lower() == "cpu":
            return await self.__loop.run_in_executor(self.__executor_cpu, exec_func)
        else:
            return await self.__loop.run_in_executor(self.__executor_io, exec_func)

    def gather(self, *coro) -> asyncio.Future:
        return asyncio.gather(*coro)

    async def wait(self, *coro: Union[Coroutine, asyncio.Future]) -> list:
        return (await asyncio.wait(coro))[0]

    async def next(self, time: float=0):
        asyncio.sleep(time)

    def application(self) -> "Application":
        """Returns the Application"""
        return self.__application

    def program(self, program: "Program"):
        """Set the Program to have Focus"""
        self.schedule(self.__application.program(program))

    def render(self, obj: "Primative"):
        """Render Primative"""
        return self.__application.render.submit(obj)

    class interval:
        """Call func repeatedly, determinded by repeat, with a delay in seconds"""

        def __init__(self, func: callable, delay: float=1, repeat: int=-1):
            """Call func repeatedly, determinded by repeat, with a delay in seconds"""
            self._cancel = False
            self._event = asyncio.Event()
            self._event.set()
            self.func = func
            self.delay = delay
            self.repeat = repeat
            self._fut = interface.schedule(self.run())

        def cancel(self):
            """Cancel the interval"""
            self._cancel = True

        def pause(self):
            self._event.clear()
        def resume(self):
            self._event.set()

        def __await__(self):
            return self._fut.__await__()

        def __str__(self):
            return f"Interval{self.func}"

        async def run(self):
            err_count = 0
            await asyncio.sleep(self.delay)
            while not self._cancel:
                await self._event.wait()
                try:
                    f = self.func()
                    if asyncio.iscoroutinefunction(self.func):
                        await f
                except Exception as e:
                    log.core.warning("%s - %s: %s", self, type(e).__name__, e)
                    log.traceback.error("%s", self, exc_info=e)
                    err_count += 1
                    if err_count >= 3:
                        log.core.error("Interval has thrown too many errors and has been cancelled - %s", self)
                        self.cancel()
                await asyncio.sleep(self.delay)

        def __hash__(self) -> int:
            return id(self)

Interface = Interface()
interface = Interface
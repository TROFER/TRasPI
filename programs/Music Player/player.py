import sounddevice as sd
import soundfile as sf
import asyncio
import queue
from collections import deque
from typing import Union, Awaitable
import core

class Track:

    def __init__(self, path: str):
        self.path = path
        # with sf.SoundFile(self.path, closefd=False) as file:
        #     self.__frames = int(file.frames)
        #     self.__samplerate = int(file.samplerate)

DTYPE = "float32"

class Player:

    track = Track

    def __init__(self, blocksize: int=4096, buffersize: int=8):
        self.__active = None
        self.__file = None
        self.__tracks = deque()
        self.__futures = {}
        self.__buffer = queue.Queue()
        self.__buffer_size = asyncio.Semaphore(buffersize)
        self.__event = asyncio.Event()
        self.__event.set()

        self.__SIZE_BLOCK = blocksize
        self.__SIZE_FRAME = 8 # for float32
        self.__SIZE_DATA = self.__SIZE_BLOCK * self.__SIZE_FRAME
        self.__stream = sd.RawOutputStream(blocksize=blocksize, dtype=DTYPE, callback=self.__callback, finished_callback=self.__stop_callback)

    def __await__(self):
        return self.__event.wait().__await__()

    @property
    def active(self) -> Union[None, Track]:
        return self.__active if self.__stream.active else None

    async def wait(self, track: Track) -> bool:
        if (fut := self.__futures.get(track)):
            await fut
            return True
        return False

    def append(self, track: Track, play=True) -> Awaitable:
        self.__tracks.append(track)
        fut = self.__futures[track] = core.Interface.loop.create_future()
        if play:
            self.play()
        return fut

    def play(self):
        if self.__event.is_set():
            # print("Play")
            self.__event.clear()
            core.Interface.schedule(self.__refill_buffer())

    def pause(self):
        self.__stream.stop()
        self.__event.set()
    
    def skip(self):
        self.__get_next_track()

    async def __refill_buffer(self):
        core.Interface.schedule(self.__stream.start)
        while self.__active or self.__get_next_track(): # self.__stream.active or
            await self.__buffer_size.acquire()
            data = self.__file.buffer_read(self.__SIZE_BLOCK, dtype=DTYPE)
            if len(data) < self.__SIZE_DATA:
                self.__get_next_track()
            self.__buffer.put(data)
        self.pause()

    def __get_next_track(self):
        if (fut := self.__futures.pop(self.__active, False)):
            fut.set_result(True)

        if self.__file:
            core.Interface.schedule(self.__file.close)

        if not self.__tracks:
            self.__active = None
            self.pause()
            return False

        track = self.__tracks.popleft()
        self.__active = track
        try:
            self.__file = sf.SoundFile(track.path)
        except FileNotFoundError:
            return self.__get_next_track()
        return True

    def __callback(self, outdata: list, frames: int, time_info, status: sd.CallbackFlags):
        if status:
            print("SoundPlayer Status:", status)
        try:
            data = self.__buffer.get_nowait()
        except asyncio.QueueEmpty as e:
            print("Buffer Empty")
            return

        if len(data) < self.__SIZE_DATA:
            # print("Missing Data", self.__SIZE_DATA - len(data))
            outdata[:len(data)] = data
            outdata[len(data):] = b"\x00" * (self.__SIZE_DATA - len(data))
            # core.Interface.loop.call_soon_threadsafe(self.__get_next_track)
        else:
            outdata[:] = data

        self.__buffer.task_done()
        core.Interface.loop.call_soon_threadsafe(self.__buffer_size.release)

    def __stop_callback(self):
        # print("Stop")
        core.Interface.loop.call_soon_threadsafe(self.__event.set)

player = Player()
# t1 = Track("Music/s1.wav")
# t2 = Track("Music/s2.wav")

# async def main():
#      player.append(t1)
#      player.play()
#      player.append(t2)
#      await player
#      s = player.append(t1, True)
#         player.append(t2)
#         await s
#         print("T1:", s)
#         await player
#         core.Interface.stop()

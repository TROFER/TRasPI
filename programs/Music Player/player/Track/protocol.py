import asyncio
from .base import TrackBase

class TrackStream(TrackBase):
    def __init__(self, stream: asyncio.StreamReader):
        super().__init__()
        self.stream = stream

    async def _read(self, size: int) -> list:
        return await self.stream.read(size * self._size)

    async def _preload(self, stream: 'sd.RawOutputStream', block: int):
        self._size = stream.channels * stream.samplesize
        self.stream._limit = block * self._size
        self.stream._maybe_resume_transport()
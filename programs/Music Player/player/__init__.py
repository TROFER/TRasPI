from .Player import Player
from .Status import Status
from .Track import Track, TrackBase

__all__ = ["Player", "Track", "Status", "TrackBase"]

main = Player(samplerate=48000, blocksize=8192, buffersize=16)
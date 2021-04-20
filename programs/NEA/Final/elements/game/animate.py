import time

import core


class Animation:

    def __init__(self, mode: str, frames: list, speed: float):
        self.mode = True if mode == "image" else False
        self.frames = frames
        self.speed = speed
        self.index = 0 
        self.current_frame = self.frames[0]
        self.frame_time = time.time()
     
    def render(self, frame):
        if time.time() - self.frame_time > self.speed:
            self.next_frame()
            self.frame_time = time.time()

        if self.mode:
            frame.alpha_composite(self.current_frame)
        else:
            core.hw.Backlight.fill(self.frames[self.index], hsv=False, force=True)

        return frame
    
    def next_frame(self):
        if self.index + 1 > len(self.frames) - 1:
            self.index = 0
        else:
            self.index += 1
        self.current_frame = self.frames[self.index]
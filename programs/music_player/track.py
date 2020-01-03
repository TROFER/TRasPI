import core

class Track:

    def __init__(self, path):
        self.path = f"{core.sys.PATH}user/music/{path}"
        self.name = path[:len(path)-4]
        self.description = f"{' '*3}{self.name}{' '*3}"

    def length(self):
        return self.track.get_length()

    def info(self):
        return self.description

    def path(self):
        return self.path

    def play(self):
        self.track = pygame.mixer.Sound(self.path)
        self.track.play()

    def unpause(self):
        pygame.mixer.unpause()

    def pause(self):
        self.track.pause()

    def stop(self):
        self.track.stop()

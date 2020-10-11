import subprocess
from ..interface import Interface

class Process(subprocess.Popen):

    PIPE = subprocess.PIPE
    STDOUT = subprocess.STDOUT
    DEVNULL = subprocess.DEVNULL

    def __init__(self, args, stdout=None, stderr=None, stdin=None, shell=False,  **kwargs):
        super().__init__(args, stdout=stdout, stderr=stderr, stdin=stdin, shell=shell, **kwargs)

    def __await__(self):
        return self.read().__await__()

    async def read(self) -> subprocess.CompletedProcess:
        while self.poll() is None:
            await Interface.next()
        return subprocess.CompletedProcess(self.args, self.returncode, self.stdout.read() if self.stdout else None, self.stderr.read() if self.stderr else None)

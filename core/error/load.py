from core.error.base import Load, _fmt_exc, _fmt_exc_only
import traceback

class ImportApp(Load):

    def __init__(self, name: str, path: str):
        self.name, self.path = name, path

    def __str__(self) -> str:
        return f"'{self.name}' from '{self.path}'"

class ModuleFileImport(ImportApp):

    def __str__(self) -> str:
        x = f"Failed to Import Application {super().__str__()} cause {_fmt_exc_only(self.__cause__)}\nFull Cause: {_fmt_exc(self.err)}"
        print(x)
        return f"Failed to Import Application {super().__str__()} cause {_fmt_exc_only(self.__cause__)}\nFull Cause: {_fmt_exc(self.err)}"

class Validate(ImportApp):

    def __init__(self, name: str, path: str, reason: str="INVALID"):
        super().__init__(name, path)
        self.reason = reason

    def __str__(self) -> str:
        return f"Unable to Validate Application {super().__str__()} as {self.reason}"

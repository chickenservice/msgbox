import time

from msgbox import MsgBox, PoisonPill


class FuncBox(MsgBox):
    def __init__(self):
        super().__init__()
        self._count = 0

    def handle(self, msg):
        match msg:
            case "add":
                time.sleep(1)
                self._count += 1
            case "get":
                return self._count


if __name__ == "__main__":
    f = FuncBox()
    f.post("add")
    f.post("add")
    f.post("add")
    f.post("add")
    f.post(PoisonPill())
    f.post("add")
    assert f.ask("get") == 4
    f.shutdown()



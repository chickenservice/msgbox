import time

from msgbox import MsgBox, PoisonPill, recurring_scheduler


class FuncBox(MsgBox):
    def __init__(self, delay=1):
        super().__init__()
        self._count = 0
        self._respond = False
        self._objs = []
        self._pinger = True
        recurring_scheduler(delay, self, "respond")

    def handle(self, msg):
        match msg:
            case ("ping", obj):
                print(f"{self} recv ping from {obj}")
                self._pinger = False
                self._objs.append(obj)
            case ("pong", obj):
                print(f"{self} recv pong from {obj}")
                self._pinger = True
                self._objs.append(obj)
            case "respond":
                for o in self._objs:
                    print(f"{self} answer pong")
                    o.post(("ping" if self._pinger else "pong", self))
                self._objs.clear()


if __name__ == "__main__":
    a = FuncBox(1)
    b = FuncBox(0.5)
    c = FuncBox(2)
    a.post(('ping', b))
    c.post(('ping', a))
    c.post(('ping', b))
    time.sleep(5)
    a.post(PoisonPill)
    b.post(PoisonPill)
    c.post(PoisonPill)

    MsgBox.shutdown()


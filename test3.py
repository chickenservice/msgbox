import time

from msgbox import MsgBox, PoisonPill


class Stateful(MsgBox):
    def handle(self, msg):
        print('handle')
        if msg == 'a':
            self.become(self.a)

    def a(self, msg):
        print('a')
        if msg == 'h':
            self.become(self.handle)


if __name__ == "__main__":
    s = Stateful()
    s.post('xyz')
    s.post('a')
    s.post('xyz')
    s.post('h')
    s.post('xyz')

    time.sleep(2)

    s.post(PoisonPill())


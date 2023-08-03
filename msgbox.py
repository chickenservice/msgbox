"""
Copyright 2023 Alessio Eberl

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

import concurrent.futures
import queue
import threading


class PoisonPill:
    pass


class PeriodicTimer:
    def __init__(self, interval, mbox, msg):
        self._handle = None
        self._cancelled = False
        self._timer(interval, mbox, msg)

    def _timer(self, interval, mbox, msg):
        def __timer():
            if self._cancelled:
                return
            mbox.post(self._msg)
            self._handle = threading.Timer(interval, __timer)
            self._handle.start()

        __timer()

    def stop(self):
        self._cancelled = True
        self._curr.cancel()


def single_timer(delay, mbox, msg):
    def _run():
        mbox.post(msg)

    timer = threading.Timer(delay, _run)
    timer.start()


class MsgBox:
    exec = concurrent.futures.ThreadPoolExecutor()

    def __init__(self):
        self._q = queue.Queue()
        self._busy = False
        self._stopped = False
        self._lock = threading.Lock()
        self._futures = []

    def _run(self):
        self._busy = True
        try:
            msg = self._q.get(False)
        except:
            self._busy = False
            self._lock.release()
            return

        if isinstance(msg[0], PoisonPill):
            for future in self._futures:
                future.cancel()
            while self._q.not_empty:
                msg = self._q.get(False)
                if msg[1]:
                    msg[1].cancel()

            self._futures.clear()
            self._stopped = True
            self._lock.release()
            return

        future = self.exec.submit(self.handle, msg[0])
        def l(_):
            self._busy = False
        def r(_):
            self._lock.acquire()
            self._run()

        self._lock.release()
        future.add_done_callback(l)
        future.add_done_callback(r)
        if msg[1]:
            self._futures.append(msg[1])
            future.add_done_callback(lambda f: msg[1].set_result(f.result()))

    def post(self, msg):
        if self._stopped:
            return
        self._q.put((msg, None))
        self._lock.acquire()
        if not self._busy and not self._stopped:
            self._run()
        else:
            self._lock.release()

    def ask(self, msg):
        if self._stopped:
            return
        result = concurrent.futures.Future()
        self._q.put((msg, result))
        self._lock.acquire()
        if not self._busy and not self._stopped:
            self._run()
        else:
            self._lock.release()

        return result.result()

    def handle(self, msg):
        pass

    @classmethod
    def shutdown(cls):
        cls.exec.shutdown()

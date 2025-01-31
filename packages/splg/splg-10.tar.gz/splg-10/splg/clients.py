# This file is placed in the Public Domain.
# pylint: disable=C0115,C0116,R0903,W0105,W0212,W0613,W0718,E0402


"clients"


import queue
import threading


from .runtime import Default, Fleet, Reactor, launch


"config"


class Config(Default):

    init = "irc,mdl,rss"
    name = Default.__module__.rsplit(".", maxsplit=2)[-2]
    opts = Default()


"client"


class Client(Reactor):

    def __init__(self):
        Reactor.__init__(self)
        Fleet.add(self)

    def raw(self, txt) -> None:
        raise NotImplementedError("raw")

    def say(self, channel, txt) -> None:
        self.raw(txt)


"output"


class Output:

    def __init__(self):
        self.oqueue   = queue.Queue()
        self.running = threading.Event()

    def loop(self) -> None:
        self.running.set()
        while self.running.is_set():
            evt = self.oqueue.get()
            if evt is None:
                self.oqueue.task_done()
                break
            Fleet.display(evt)
            self.oqueue.task_done()

    def oput(self,evt) -> None:
        if not self.running.is_set():
            Fleet.display(evt)
        self.oqueue.put(evt)

    def start(self) -> None:
        if not self.running.is_set():
            self.running.set()
            launch(self.loop)

    def stop(self) -> None:
        self.running.clear()
        self.oqueue.put(None)

    def wait(self) -> None:
        self.oqueue.join()


"buffered"


class Buffered(Client, Output):

    def __init__(self):
        Client.__init__(self)
        Output.__init__(self)

    def raw(self, txt) -> None:
        raise NotImplementedError("raw")

    def start(self) -> None:
        Output.start(self)
        Client.start(self)

    def stop(self) -> None:
        Client.stop(self)
        Output.stop(self)

    def wait(self) -> None:
        Client.wait(self)
        Output.wait(self)


"utilities"


def debug(txt) -> None:
    if "v" in Config.opts:
        output(txt)


def output(txt) -> None:
    # output here
    print(txt)


"interface"


def __dir__():
    return (
        'Default',
        'Client',
        'Event',
        'Fleet',
        'debug'
    )


__all__ = __dir__()

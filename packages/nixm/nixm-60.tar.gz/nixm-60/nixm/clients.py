# This file is placed in the Public Domain.
# pylint: disable=C0115,C0116,R0903,W0105,W0212,W0613,W0718,E0402


"clients"


import queue
import threading


from .runtime import Default, Fleet, Reactor, launch


class Config(Default):

    init = "irc,rss"
    name = Default.__module__.rsplit(".", maxsplit=2)[-2]
    opts = Default()


class Client(Reactor):

    def __init__(self):
        Reactor.__init__(self)
        Fleet.add(self)

    def raw(self, txt):
        raise NotImplementedError("raw")

    def say(self, channel, txt):
        self.raw(txt)


class Output:

    def __init__(self):
        self.oqueue   = queue.Queue()
        self.running = threading.Event()

    def loop(self):
        self.running.set()
        while self.running.is_set():
            evt = self.oqueue.get()
            if evt is None:
                self.oqueue.task_done()
                break
            Fleet.display(evt)
            self.oqueue.task_done()

    def oput(self,evt):
        if not self.running.is_set():
            Fleet.display(evt)
        self.oqueue.put(evt)

    def start(self):
        if not self.running.is_set():
            self.running.set()
            launch(self.loop)

    def stop(self):
        self.running.clear()
        self.oqueue.put(None)

    def wait(self):
        self.oqueue.join()


class Buffered(Client, Output):

    def __init__(self):
        Client.__init__(self)
        Output.__init__(self)

    def raw(self, txt):
        raise NotImplementedError("raw")

    def start(self):
        Output.start(self)
        Client.start(self)

    def stop(self):
        Client.stop(self)
        Output.stop(self)

    def wait(self):
        Client.wait(self)
        Output.wait(self)


def __dir__():
    return (
        'Default',
        'Client',
        'Event',
        'Fleet'
    )

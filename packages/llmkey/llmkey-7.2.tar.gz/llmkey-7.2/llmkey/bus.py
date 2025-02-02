import json
import logging

from . import tk_tools

logger = logging.getLogger("bus")


class Bus:
    def __init__(self, tk_root):
        self.tk_root = tk_root

    def send(self, event, *, data=None):
        logger.debug("Sending %r data=%r", event, data)
        if data is not None:
            self.tk_root.event_generate(event, data=json.dumps(data))
        else:
            self.tk_root.event_generate(event)

    def bind(self, event, callback):
        tk_tools.my_bind(self.tk_root, event, callback)


class MockBus:
    def send(self, event, *, data=None):
        print("Sending", event, data)


    def bind(self, *_):
        raise NotImplementedError()

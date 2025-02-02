import threading
import logging
import traceback

from .bus import Bus

class LlmRunner:
    "Single threaded worker to run queries"

    def __init__(self, bus: Bus):
        self.bus = bus
        self.thread = None

    @property
    def running(self):
        return self.thread is not None

    def run(self, f, event):
        def wrapped():
            try:
                result = f()
            except Exception: #pylint: disable=broad-except
                logging.exception("LLM command failed")
                message = traceback.format_exc()
                self.bus.send("<<failed>>", data={"message": message})
                self.thread = None
            else:
                self.thread = None
                self.bus.send(event, data={"result": result})


        if not self.thread:
            self.thread = threading.Thread(target=wrapped)
            self.thread.daemon = True
            self.thread.start()
            return True
        else:
            return False

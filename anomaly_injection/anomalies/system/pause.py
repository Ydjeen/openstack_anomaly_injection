import threading
from ..anomaly import Anomaly
from time import sleep


class PauseAnomaly(Anomaly):
    def __init__(self, params, targets, conn, *args, **kwargs):
        self.duration = self.delay = None
        super().__init__(params, targets, conn)

    def _unpack_params(self, params):
        # TODO: add logic for min sec etc...
        self.duration = int(params['duration'])
        self.delay = int(params['delay'])

    def run(self):
        sleep(self.delay)
        for target in self.targets:
            target.stop()
            threading.Timer(self.duration, target.start).start()
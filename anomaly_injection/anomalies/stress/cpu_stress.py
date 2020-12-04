import threading
from ..anomaly import Anomaly
from time import sleep


class CpuStressAnomaly(Anomaly):
    def __init__(self, params, targets, conn, *args, **kwargs):
        self.duration = self.delay = None
        super().__init__(params, targets, conn)

    def _unpack_params(self, params):
        pass

    def run(self):
        sleep(self.delay)
        for target in self.targets:
            target.stop()
            threading.Timer(self.duration, target.stres).start()

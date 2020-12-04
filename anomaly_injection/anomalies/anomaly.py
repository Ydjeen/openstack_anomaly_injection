import os
from datetime import datetime


class Anomaly:
    def __init__(self, params, targets, conn, *args, **kwargs):
        self.conn = conn
        self.targets = self._get_targets(targets)
        self._unpack_params(params)

    def run(self):
        raise NotImplementedError

    def _unpack_params(self, params):
        raise NotImplementedError

    def _get_targets(self, targets):
        target_objs = []
        for target in targets:
            target_objs.append(self.conn.get_target(target))
        return target_objs


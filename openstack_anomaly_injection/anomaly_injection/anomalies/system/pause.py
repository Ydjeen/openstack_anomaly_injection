import threading
from . import Anomaly
from ..utils import convert_time_to_s

import logging

log_info = logging.getLogger('infoLog')
log_error = logging.getLogger('errorLog')
log_debug = logging.getLogger('debuggerLog')
log_status = logging.getLogger('statusLog')


class PauseAnomaly(Anomaly):
    """
    Pause anomaly is used for simulating... TODO INSERT TEXT.

    :param params: Anomaly specific parameters
    :type params: dict
    :param target: Target object of the anomaly
    :type target: Object
    :param conn: Cloud connection object
    :type conn: :class:`.node_control.connection.CloudConnection`
    """

    def __init__(self, params, target, conn, *args, **kwargs):
        supported_targets = ["deployment", "container", "host"]
        name = "Pause"
        super().__init__(params, target, conn, supported_targets=supported_targets, name=name)

    def _unpack_params(self, params):
        self.duration = convert_time_to_s(params.get('duration', '0s'))
        self.delay = convert_time_to_s(params.get('delay', '0s'))

    def _run(self):
        self.target.stop()
        threading.Timer(self.duration, self.target.start).start()

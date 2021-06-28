import logging
from time import sleep

from anomalies.utils import convert_time_to_s

log_info = logging.getLogger('infoLog')
log_error = logging.getLogger('errorLog')
log_debug = logging.getLogger('debuggerLog')


class Anomaly:
    """
    Base anomaly class.

    Each Anomaly should implement the ``_run()`` method, which should contain the logic for running the anomaly.
    Delay should not be implemented in the method, as it is already implemented in ``run()`` and is the same for all
    anomalies.

    Each Anomaly should implement the ``_unpack_params()`` method, which should contain the logic for unpacking the
    anomaly-specific parameters.

    :param params: Anomaly specific parameters
    :type params: dict
    :param target: Target object of the anomaly
    :type target: Object
    :param conn: Cloud connection object
    :type conn: :class:`.node_control.connection.CloudConnection`
    :param supported_targets: List of targets that the anomaly supports
            Ex. ["deployment", "container", "host","network"]
    :type supported_targets: list
    """

    def __init__(self, params, target, conn, supported_targets=None, name="", *args, **kwargs):
        self.conn = conn
        self.name = name
        self._delay = params.get('delay', '0s')
        self._duration = params.get('duration', '0s')
        self.supported_targets = supported_targets or list()

        _target = target.get('target')
        if _target not in self.supported_targets:
            raise Exception(f"Target {_target} not supported for anomaly {self.name}")
        self.target = self.conn.get_target(target.get('target'), host=target.get('host'), id=target.get('id'),
                                           name=target.get('name'), interface=target.get('interface'))
        self._unpack_params(params)

    @property
    def duration(self):
        return convert_time_to_s(self._duration)

    @property
    def delay(self):
        return convert_time_to_s(self._delay)

    def run(self):
        """Default method for running anomalies.
        Implements the delay before executing the anomaly."""
        log_info.info(
            f"Injecting {self.name} anomaly for {self._duration} after {self._delay} on {self.target}")
        sleep(self.delay)
        self._run()
        log_info.info(f"{self.name} anomaly executed successfully")

    def _run(self):
        """Logic for executing specific anomaly"""
        raise NotImplementedError

    def _unpack_params(self, params):
        """Logic for unpacking anomaly specific parameters"""
        raise NotImplementedError

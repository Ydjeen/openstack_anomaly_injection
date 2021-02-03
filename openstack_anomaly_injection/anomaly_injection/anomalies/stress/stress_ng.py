from . import Anomaly


class StressNgAnomaly(Anomaly):
    """ StressNgAnomaly uses the Stress-ng module to stress test a target in various selectable ways.
    It supports a wide range of CPU, memory, I/O specific stress tests. For more info go to
    https://manpages.ubuntu.com/manpages/artful/man1/stress-ng.1.html

    :param params: Anomaly specific parameters
    :type params: dict
    :param target: Target object of the anomaly
    :type target: Object
    :param conn: Cloud connection object
    :type conn: :class:`.node_control.connection.CloudConnection`
    """

    def __init__(self, params, target, conn, *args, **kwargs):
        supported_targets = ["deployment", "container", "host", "node"]
        name = "Stress-ng"
        super().__init__(params, target, conn, supported_targets=supported_targets, name=name)

    def _unpack_params(self, params):
        # noinspection PyTypeChecker
        self.params = " ".join([params.get('stressors', ""), "-t " + params.get('duration')])

    def _run(self):
        self.target.stress(self.params)

import tempfile
import os
import stat
from oslo_concurrency import processutils
import shlex

from . import Anomaly


class TCAnomaly(Anomaly):
    """
    :param params: Anomaly specific parameters
    :type params: dict
    :param target: Target object of the anomaly
    :type target: Object
    :param conn: Cloud connection object
    :type conn: :class:`.node_control.connection.CloudConnection`
    """

    def __init__(self, params, target, conn, *args, **kwargs):
        supported_targets = ["network"]
        name = "TC"
        super().__init__(params, target, conn, supported_targets=supported_targets, name=name)

    def _unpack_params(self, params):
        # noinspection PyTypeChecker
        self.param_string = params.get("tcconfig", None)
        if not self.param_string:
            self.param_string = ""
            for key, val in params.items():
                self.param_string = " ".join([self.param_string, "--" + key, str(val)]).strip()

        print(self.target.__class__.__name__)
        if self.target.__class__.__name__ == "Container":
            self.param_string = " ".join([self.param_string, "--docker", str(self.target.id)]).strip()
        else:
            self.param_string += " "
            self.param_string += self.target.device

    def _run(self):
        temp_dir = tempfile.mkdtemp(prefix='temp_files')
        anomaly_file_name = f'{temp_dir}/tcanomaly.sh'
        with open(anomaly_file_name, 'w') as fd:
            print("tcset --delay 100ms lo", file=fd)
            # print("tcset", self.param_string, file=fd)
            # print("sleep", self.duration, file=fd)
            # print("tcdel", self.param_string, file=fd)
            # print("echo bunnies")

        st = os.stat(anomaly_file_name)
        os.chmod(anomaly_file_name, st.st_mode | stat.S_IEXEC)
        self.target.script(anomaly_file_name)

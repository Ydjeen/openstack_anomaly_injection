from .node_control import CloudConnection
from .anomalies.system import PauseAnomaly
from .anomalies.stress import StressNgAnomaly
from .anomalies.network import TCAnomaly


class AnomalyInjector:
    """
    Anomaly injector class. This class prepares anomaly objects and runs them against the target deployment.

    :param cloud_config:
    :type cloud_config: dict
    :param anomalies: Cloud configuration parameters for connecting to the deployment.
    :type list <dict>: List of anomaly configurations
    """
    _anomaly_cls = {"pause": PauseAnomaly, "stress-ng": StressNgAnomaly, "tc": TCAnomaly}

    def __init__(self, cloud_config, anomalies):
        self.cloud_config = cloud_config
        conn = CloudConnection(cloud_config)
        if not isinstance(anomalies, list):
            anomalies = [anomalies]
        self.anomalies = [self._anomaly_cls[anomaly['name']](**anomaly, conn=conn) for anomaly in anomalies]

    def run(self):
        """Run the injector with the preconfigured anomalies"""
        for anomaly in self.anomalies:
            anomaly.run()

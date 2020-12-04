from node_control import CloudManagement
from .anomalies.system.pause import PauseAnomaly


class AnomalyInjector:
    anomaly_cls = {"pause": PauseAnomaly}

    def __init__(self, cloud_config, anomaly):
        self.cloud_config = cloud_config
        conn = CloudManagement(cloud_config)
        self.anomaly = self.anomaly_cls[anomaly['name']](**anomaly, conn=conn)

    def run(self):
        self.anomaly.run()

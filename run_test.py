import json
from anomaly_injection.AnomalyInjector import AnomalyInjector

cfg = json.load(open("/home/petar/work/chaos_toolkit/openstack_anomaly_injection/anomaly_injection/anomaly_config.json", 'r'))

injector = AnomalyInjector(**cfg)
injector.run()

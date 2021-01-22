from setuptools import setup

setup(
    name='chaos_toolkit',
    version='0.1',
    packages=['docs', 'docs.source', 'anomaly_injection', 'anomaly_injection.config',
              'anomaly_injection.config.argparser', 'anomaly_injection.anomalies', 'anomaly_injection.anomalies.stress',
              'anomaly_injection.anomalies.system', 'anomaly_injection.anomalies.network',
              'anomaly_injection.node_control', 'anomaly_injection.node_control.api',
              'anomaly_injection.node_control.config', 'anomaly_injection.node_control.drivers'],
    package_dir={'': 'openstack_anomaly_injection'},
    url='',
    license='non',
    author='petar',
    author_email='petar.ilijevski@campus.tu-berlin.de',
    description=''
)

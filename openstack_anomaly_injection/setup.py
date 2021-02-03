from setuptools import setup, find_packages

setup(
    name='anomaly_injection',
    version='0.1',
    packages=find_packages(exclude=('tests', 'docs')),
    package_dir={'': '../openstack_anomaly_injection'},
    url='',
    license='non',
    author='petar',
    author_email='petar.ilijevski@campus.tu-berlin.de',
    description='Anomaly injection toolkit for openstack',
    python_requires='>=3.6',
    entry_points={
        'console_scripts': ['chaos=anomaly_injection.cli:main'],
    },
    package_data={
        'anomaly_injection.config': ["*.json", "*.ini"],
        'anomaly_injection.node_control.config': ["*.json", "*.ini"]
    },
    include_package_data=True
)

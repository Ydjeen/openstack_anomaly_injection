from .errors import ContainerException, DriverException
from ..drivers import DockerContainer


class Container:
    """Container object which represents a container on the deployment.

    :param id: Container ID
    :type id: str
    :param host: Host name
    :type host: str
    :param image: Image ID
    :type image: str
    :param command: Command when starting the container
    :type command: str
    :param created: Time created
    :type created: str
    :param status: Status of container Running/Suspended
    :type status: str
    :param ports: Container ports
    :type ports: str
    :param name: Container name
    :type name: str
    :param container_driver: :class:`.drivers.DockerContainer` Driver for communicating with the container on the deployment
    :type container_driver: :class:`.drivers.DockerContainer`
    :param network_driver: Driver for communicating with the network on the deployment
    :type network_driver: object
    """
    def __init__(self, id, host, image, command, created, status, ports, name, container_driver=None,
                 network_driver=None,
                 *args, **kwargs):
        self.id = id
        self.host = host
        self.image = image
        self.command = command
        self.created = created
        self.status = status
        self.ports = ports
        self.name = name
        self.container_driver = container_driver
        self.network_driver = network_driver

    def start(self):
        """Start the container"""
        self._check_driver(self.container_driver)
        self.container_driver.start(self.name, self.host)

    def stop(self):
        """Stop the container"""
        self._check_driver(self.container_driver)
        self.container_driver.stop(self.name, self.host)

    def terminate(self):
        """Terminate the container"""
        self._check_driver(self.container_driver)
        self.container_driver.terminate(self.name, self.host)

    def restart(self):
        """Restart the container"""
        self._check_driver(self.container_driver)
        self.container_driver.restart(self.name, self.host)

    def stress(self, stressors):
        """Perform stress test on the container using stress-ng.

        :param stressors: stress-ng stressors
        :type stressors: str
        """
        self._check_driver(self.container_driver)
        self.container_driver.stress(self.name, self.host, stressors)

    @staticmethod
    def _check_driver(driver):
        if driver is None:
            raise ContainerException("Driver must be provided in order to use this function")

    def __repr__(self):
        return self.id[:10]

    def __str__(self):
        return f"Host: {self.host} - Name: {self.name} - ID: {self.id}"

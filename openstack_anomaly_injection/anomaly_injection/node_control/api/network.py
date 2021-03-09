# should contain network interfaces
from .errors import NetworkException


class Network:
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
    :param container_driver: :class:`.drivers.DockerContainer` Driver for communicating with the container
    :type container_driver: :class:`.drivers.DockerContainer`
    :param network_driver: Driver for communicating with the network on the deployment
    :type network_driver: :class:`.drivers.NetworkDriver`
    """

    def __init__(self, host, device, ipv4=None, ipv6=None, macaddress=None, mtu=None, promisc=None, stp=None, type=None,
                 speed=None, network_driver=None,
                 **kwargs):
        """

        :param host: Hostname
        :type host: str
        :param device: Name of interface
        :type device: str
        :param ipv4: IPv4 params. Contains [address,broadcast,netmask,network]
        :type ipv4: dict, optional
        :param ipv6: IPv6 params. Contains [address, prefix, scope]
        :type ipv6: dict, optional
        :param macaddress: Mac address of interface
        :type macaddress: str, optional
        :param mtu: Maximum transmission unit
        :type mtu: int, optional
        :param promisc: Promiscuous mode.
        :type promisc: bool, optional
        :param stp: Spanning tree protocol
        :type bool: bool, optional
        :param type: Type of network interface
        :type type: str
        :param speed: Maximum network speed
        :type speed: int
        :param network_driver: Driver for running network commands
        :type network_driver: :class:`.drivers.NetworkDriver`
        """
        self.host = host
        self.device = device
        self.ipv4 = ipv4
        self.ipv6 = ipv6
        self.macaddress = macaddress
        self.mtu = mtu
        self.promisc = promisc
        self.stp = stp
        self.type = type
        self.speed = speed
        self.network_driver = None,
        self.network_driver = network_driver
        self.kwargs = kwargs

    @staticmethod
    def _check_driver(driver):
        if driver is None:
            raise NetworkException("Driver must be provided in order to use this function")

    def script(self, filename):
        """Run a script on target Network

        :param filename: Path to file on local disk
        :type filename: str
        """
        self._check_driver(self.network_driver)
        return self.network_driver.script(self.device, self.host, filename)

    def __repr__(self):
        return self.device

    def __str__(self):
        return f"Host: {self.host} - Device: {self.device}"

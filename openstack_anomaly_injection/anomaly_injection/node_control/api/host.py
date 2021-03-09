class Host:
    """Host object representing a host on the deployment.

    :param ip: Host IP
    :type ip: str
    :param driver: Driver for executing host commands on the deployment.
    :type driver: :class:`.drivers.HostDriver`
    :param containers: Dictionary of :class:`.container.Container` objects available on the host.
    :type containers: dict
    :param host_info: Additional info about the host gathered from discover_hosts.
    :type host_info: str

    """

    def __init__(self, ip, containers=None, host_info=None, driver=None, networks=None):
        self.ip = ip
        self.driver = driver
        self.containers = containers or {}
        self.host_info = host_info or {}
        self.networks = networks or {}

    def __repr__(self):
        return self.ip

    def __str__(self):
        return self.ip

    def init_networks(self, networks):
        if len(self.networks) == 0:
            self.networks = networks
        else:
            raise Exception("Networks already initialized.")

    def list_containers(self):
        """List the available containers on the host"""
        return [cont.name for key, cont in self.containers.items()]

    def list_networks(self):
        """List the available containers on the host"""
        return [net.device for net in self.networks]

    def get_container(self, container_id=None, name=None):
        """
        Get a container from the host. Can provide either container id or name.

        :param container_id: ID of the container. Can be partial or full id.
        :type container_id: str, optional
        :param name: Container name.
        :type name: str, optional

        :returns:  Target Docker Container object
        :rtype:  :class:`.container.Container`
        """
        if name is None:
            full_id = [x.id for x in self.containers.values() if container_id in x.id]
            _p = f"id : {container_id}"
        elif container_id is None:
            full_id = [x.id for x in self.containers.values() if name in x.name]
            _p = f"name : {name}"
        else:
            raise Exception("Must provide container id or container_name")
        if len(full_id) == 0:
            raise Exception(f"Container {_p} not found on host {self.ip}")
        return self.containers[full_id[0]]

    def stress(self, stressors):
        """Perform stress-test on the host.

        :param stressors: Stressors available from the stress-ng module.
        :type stressors: str
        """
        self.driver.stress(self.ip, stressors)

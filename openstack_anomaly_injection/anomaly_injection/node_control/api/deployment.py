from ..drivers import DeploymentDriver


class Deployment:
    """
    Deployment object which represents the target openstack deployment

    :param hosts: Dictionary of available hosts on the deployment.
    :type hosts: dict
    :param driver: Driver for executing commands on the deployment.
    :type driver: :class:`.drivers.DeploymentDriver`
    :param deployment_info: Information about the deployment. This is gathered from host discovery.
    :type deployment_info: str

    """

    def __init__(self, hosts, driver, deployment_info=None):
        self._hosts = hosts
        self.driver = driver
        self.deployment_info = deployment_info

    @property
    def hosts(self):
        """
        Sorted list of available host objects.
        """
        return sorted(self._hosts)

    def __len__(self):
        return len(self.hosts)

    def __getitem__(self, item):
        return self.hosts[item]

    def get_ips(self):
        """
        Get the IP addresses of the available hosts.

        :returns: List of host IPs
        :rtype: list

        """
        return [host for host in self._hosts.keys()]

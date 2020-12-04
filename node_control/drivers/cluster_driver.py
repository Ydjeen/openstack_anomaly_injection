import logging

LOG = logging.getLogger(__file__)


class ClusterDriver:
    def __init__(self, ansible):
        self.ansible = ansible

    def reboot(self, hosts):
        """Reboot all nodes gracefully

        """
        LOG.info('Reboot cluster: %s', self)
        task = {
            'command': 'reboot now',
            'become': 'yes',
        }
        # note that all errors are ignored
        self.ansible.execute_on_cloud(hosts, task,
                                      raise_on_error=False)

    def poweroff(self, hosts):
        """Power off all nodes abruptly

        """
        LOG.info('Power off nodes: %s', self)
        self.ansible.execute.poweroff(hosts)

    def poweron(self):
        """Power on all nodes abruptly

        """
        LOG.info('Power on nodes: %s', self)
        self.cloud_management.power_manager.poweron(self.hosts)

    def reset(self):
        """Reset (cold restart) all nodes

        """
        LOG.info('Reset nodes: %s', self)
        self.cloud_management.power_manager.reset(self.hosts)

    def shutdown(self):
        """Shutdown all nodes gracefully

        """
        LOG.info('Shutdown nodes: %s', self)
        self.cloud_management.power_manager.shutdown(self.hosts)

    def snapshot(self, snapshot_name, suspend=True):
        """Create snapshot for all nodes

        """
        LOG.info('Create snapshot "%s" for nodes: %s', snapshot_name, self)
        self.cloud_management.power_manager.snapshot(
            self.hosts, snapshot_name, suspend)

    def revert(self, snapshot_name, resume=True):
        """Revert snapshot for all nodes

        """
        LOG.info('Revert snapshot "%s" for nodes: %s', snapshot_name, self)
        self.cloud_management.power_manager.revert(
            self.hosts, snapshot_name, resume)

    def disconnect(self, network_name):
        """Disconnect nodes from <network_name> network

        :param network_name: name of network
        """
        raise NotImplementedError

    def connect(self, network_name):
        """Connect nodes to <network_name> network

        :param network_name: name of network
        """
        raise NotImplementedError

    def stress(self, target, duration=None):
        """Stress node OS and hardware

        """

    pass

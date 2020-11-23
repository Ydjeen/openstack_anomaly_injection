def run_task(self, task, raise_on_error=True):
    """Run ansible task on node colection

    :param task: ansible task as dict
    :param raise_on_error: throw exception in case of error
    :return: AnsibleExecutionRecord with results of task
    """
    LOG.info('Run task: %s on nodes: %s', task, self)
    return self.cloud_management.execute_on_cloud(
        self.hosts, task, raise_on_error=raise_on_error)


@public
def reboot(self):
    """Reboot all nodes gracefully

    """
    LOG.info('Reboot nodes: %s', self)
    task = {
        'command': 'reboot now',
        'become': 'yes',
    }
    # note that all errors are ignored
    self.cloud_management.execute_on_cloud(self.hosts, task,
                                           raise_on_error=False)


@public
def poweroff(self):
    """Power off all nodes abruptly

    """
    LOG.info('Power off nodes: %s', self)
    self.cloud_management.power_manager.poweroff(self.hosts)


@public
def poweron(self):
    """Power on all nodes abruptly

    """
    LOG.info('Power on nodes: %s', self)
    self.cloud_management.power_manager.poweron(self.hosts)


@public
def reset(self):
    """Reset (cold restart) all nodes

    """
    LOG.info('Reset nodes: %s', self)
    self.cloud_management.power_manager.reset(self.hosts)


@public
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


@public
def disconnect(self, network_name):
    """Disconnect nodes from <network_name> network

    :param network_name: name of network
    """
    raise NotImplementedError


@public
def connect(self, network_name):
    """Connect nodes to <network_name> network

    :param network_name: name of network
    """
    raise NotImplementedError


@public
def stress(self, target, duration=None):
    """Stress node OS and hardware

    """
    duration = duration or 10  # defaults to 10 seconds
    LOG.info('Stress %s for %ss on nodes %s', target, duration, self)
    task = {'stress': {
        'target': target,
        'duration': duration,
    }}
    self.cloud_management.execute_on_cloud(self.hosts, task)

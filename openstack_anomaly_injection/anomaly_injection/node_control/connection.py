import json
from .config.config_parser import CloudConfigParser
from .config.loggers import log_info, log_debug
from .drivers.ansible_runner import AnsibleRunner
from .drivers import *
from .api import *


class CloudConnection:
    """This class serves as a connection to the openstack deployment.

        :ivar ansible: AnsibleRunner object which serves as an interface for running Ansible tasks on the target
        deployment.
        :type ansible:class AnsibleRunner:
        :ivar hosts: Dictionary containing the hosts on the deployment ( Key->value = host_ip-> host_object)
        :type hosts: dict
        :ivar networks: Dictionary containing the available network interfaces.
        :type networks: dict
        :ivar cluster: Object representing the cluster.
        :type cluster: class: `AnsibleRunner`
        :ivar network_d: :class:`.drivers.NetworkDriver` for performing networking tasks on the deployment.
        :type network_d: class:`.drivers.NetworkDriver`
        :ivar cont_d: :class:`.drivers.DockerContainer` driver for performing container related tasks on the deployment.
        :type cont_d: class:`.drivers.DockerContainer`
        :ivar host_d: :class:`.drivers.HostDriver` for performing  tasks on the hosts.
        :type host_d: :class:`.drivers.HostDriver`
        :ivar cloud_d: :class:`.drivers.DeploymentDriver`  for performing tasks on the deployment.
        :type cloud_d: class:`.drivers.DeploymentDriver`
        :param config: Json configuration for the deployment. See cloud_config.json for example.
        :type config: dict
        :param connect:  Whether to connect to the deployment on object creation.
        :type connect: bool
        """

    def __init__(self, config, connect=True):
        self.ansible = None
        self.cluster = self.hosts = self.networks = dict()
        self.network_d = self.cont_d = self.host_d = self.cloud_d = None
        self._parse_config(config)
        self._init_drivers()
        if connect:
            self.connect()

    def _init_drivers(self):
        self.network_d = NetworkDriver(ansible_runner=self.ansible)
        self.cont_d = DockerContainer(ansible_runner=self.ansible)
        self.cloud_d = DeploymentDriver(self.ansible)
        self.host_d = HostDriver(ansible_runner=self.ansible)

    def _parse_config(self, config):
        config = CloudConfigParser().parse(config)
        self.ansible = AnsibleRunner(config['ansible'])
        self.hosts = config['hosts']

    def verify(self):
        pass

    def connect(self):
        """ Connect to the deployment.

        :return: Deployment object

        """

        hosts = self._discover_hosts()
        _hosts = " --- ".join([host.ip + " containers: " + str(len(host.containers)) for host in hosts.values()])
        log_debug.debug("Discovered hosts: " + _hosts)
        self.networks = self._discover_networks()
        _networks = " --- ".join(
            [host + ":" + str(" ".join([net.device for net in networks])) for host, networks in self.networks.items()])
        log_debug.debug("Discovered networks: " + _networks)

        for hostname, host in hosts.items():
            host.init_networks(self.networks[hostname])
        deployment = Deployment(hosts, self.cloud_d)
        self.cluster = deployment
        self.hosts = hosts
        return deployment

    def list_containers(self, host='all'):
        """
        Lists the available containers on a target host.

        :param host: Target host. If 'all' lists the containers from all of the hosts on the deployment
        :type host: str

        :return: Dictionary of container objects on the deployment. key->value = host_ip -> container list.
        :rtype: dict

        """
        log_debug.debug("Listing containers")
        result = {}
        if host == 'all':
            for host, host in self.hosts.items():
                result[host] = host.list_containers()
        else:
            result[host] = self.hosts[host].list_containers()
        return result

    def list_hosts(self):
        """
        List hosts on the deployment

        :return: Available hosts.
        :rtype: str
        """
        return str(self.hosts)

    def list_networks(self, target):
        result = {}
        host = target['host']
        if host == 'all':
            for host, host in self.hosts.items():
                result[host] = host.list_networks()
        else:
            result[host] = self.hosts[host].list_networks()
        return result

    def get_host(self, host):
        """Get the object of a target host

        :return: Host object
        :rtype: :class:`.api.Host`
        """
        if host not in self.hosts:
            raise Exception("host %s not found on cluster" % host)
        return self.hosts[host]

    def get_network(self, host, interface):
        for net in self.networks[host]:
            if net.device == interface:
                return net

        def execute_ansible(self, hosts, task):
            """
            Execute an ansible task on the deployment.

            :param hosts: List of hosts
            :type hosts: list
            :param task: Task that needs to be executed
            :type task: dict

            :return: List of Named tuples containing the 'host', 'status', 'task' and 'payload' in json format.
            :rtype: list

            """
            self.ansible.execute(hosts, task)

    def get_container(self, host, container_id=None, name=None):
        """
        Get the object of a target container

        :param host: Target host IP.
        :type host: str
        :param container_id:  Container ID
        :type container_id: str, optional
        :param name: Container name (optional)
        :type name: str, optional

        :return: Requested DockerContainer object
        :rtype: :class:`.api.Container`
        """
        if host not in self.hosts.keys():
            raise Exception("Host not found on deployment.")
        container = self.hosts[host].get_container(container_id, name)
        return container

    def get_target(self, target, host=None, id=None, name=None, interface=None):
        """
        Get the requested target from the deployment.

        :param target: Target can be either a 'host', 'container', 'deployment' or 'network'.
        :type target: str
        :param host: If the target in on a specific host, then specify hostname if target is 'network' or 'container'.
        :type host: str
        :param id:  ID of the target
        :type id: str, optional
        :param name: Target name
        :type name: str, optional
        :param interface: Target network interface
        :type interface: str, optional

        :return: Target object
        """
        log_debug.debug(f"Fetching target {target}")
        if target == 'container':
            return self.get_container(host, id, name)
        elif target in ['host', 'node']:
            return self.get_host(host)
        elif target == "network":
            return self.get_network(host, interface)
        else:
            raise Exception("Target type does not exist")

    def _unpack_host(self, host_info):
        """
        Unpack the host info into host object

        :param host_info: Information about the host
        :type host_info: NamedTuple

        :return: Target object
        :rtype: :class:`.api.Host`
        """
        host = host_info.host
        host_data = host_info.payload
        containers = dict()
        log_debug.debug(f"Unpacking containers for host {host}")
        for container_info in host_data['containers']:
            container = self._unpack_container(container_info, host)
            containers[container.id] = container
        host = Host(ip=host, containers=containers, host_info=host_info, driver=self.host_d)
        return host

    def _unpack_container(self, container_info, host):
        """
        Unpack the container info into host object

        :param container_info:  Information about the container
        :type container_info: NamedTuple
        :param host: Host of the container.
        :type host: str

        :return: Container object
        :rtype: :class:`.api.Container`
        """
        params = {"host": host, "container_driver": self.cont_d}
        for key, val in container_info.items():
            if key == "Names":
                params['name'] = val[0][1:]
            else:
                params[key.lower()] = val

        container = Container(**params)
        return container

    def perform_action(self, action, target):
        """
        Perform an action on the deployment. This function is used by the CLI.

        :param action:  Target action
        :type action: str
        :param target: Host of the container.
        :type target: str
        """
        actions = {"list": self._list_action}
        _action = actions.get(action, None)
        if not _action:
            raise Exception(f"Action {action} is not supported.")
        # noinspection PyArgumentList
        return _action(target)

    def _list_action(self, target):
        if target['target'] == "container":
            return self.list_containers(host=target.get('host'))
        elif target['target'] == "node" or target['target'] == "deployment":
            return self.list_hosts()
        elif target['target'] == "network":
            return self.list_networks(target)
        else:
            raise Exception("Invalid target")

    def _discover_hosts(self):
        # GET THIS FROM ANSIBLE
        task = {
            'docker_host_info': {
                'containers': 'yes'
            },
        }
        log_info.info("Discovering hosts")
        result = self.ansible.execute(self.hosts, task)
        # with open("cloud_info.json", 'w') as file:
        #     json.dump(result, file)
        hosts = {}
        log_debug.debug("Unpacking hosts")
        for host in result:
            _host = self._unpack_host(host)
            hosts[_host.ip] = _host
        return hosts

    def _discover_networks(self):
        task = {
            'ansible.builtin.setup': {
                'gather_subset': ['!all', 'network', "!min"]
            }}
        log_info.info("Discovering network interfaces")
        result = self.ansible.execute(self.hosts, task)
        networks = {}
        log_debug.debug("Unpacking networks")
        for host in result:
            networks[host[0]] = self._unpack_networks(host)
        return networks

    def _unpack_networks(self, host):
        networks = host.payload['ansible_facts']['ansible_interfaces']
        network_objects = list()
        for network in networks:
            network = network.replace("-", "_")
            _params = host.payload['ansible_facts'][f"ansible_{network}"]
            network_objects.append(Network(host.host, **_params, network_driver=self.network_d))

        return network_objects

import json
from node_control.config.config_parser import CloudConfigParser
from node_control.ansible_runner import AnsibleRunner
from node_control.drivers import *
from node_control.api import *


class CloudManagement:
    def __init__(self, config, connect=True):
        self.ansible = self.hosts = None
        self.cluster = self.nodes = self.containers = None
        self.network_d = self.cont_d = self.node_d = self.cloud_d = None
        self._parse_config(config)
        self._init_drivers()
        if connect:
            self.connect()

    def _init_drivers(self):
        self.network_d = NetworkDriver()  # to be implemented
        self.cont_d = DockerContainer(ansible_runner=self.ansible)
        self.cloud_d = ClusterDriver(self.ansible)  # to be implemented
        self.node_d = NodeController()  # to be implemented

    def _parse_config(self, config):
        config = CloudConfigParser().parse(config)
        self.ansible = AnsibleRunner(config['ansible'])
        self.hosts = config['hosts']

    def verify(self):
        pass

    def connect(self):
        # GET THIS FROM ANSIBLE
        task = {
            'docker_host_info': {
                'containers': 'yes'
            },
        }
        result = self.ansible.execute(self.hosts, task)
        nodes = {}
        for node in result:
            node = self.unpack_node(node)
            nodes[node.ip] = node
        cluster = Deployment(nodes, self.cloud_d, result)
        self.cluster = cluster
        self.nodes = nodes
        return cluster

    def list_containers(self, host='all'):
        result = {}
        if host == 'all':
            for host, node in self.nodes.items():
                result[host] = node.list_containers()
        else:
            result[host] = self.nodes[host].list_containers()
        return result

    def list_nodes(self, host='all'):
        return str(self.nodes)

    def get_node(self, host):
        for node in self.nodes:
            if node.ip == host:
                return node
        raise Exception("Node %s not found on cluster" % host)

    def execute_ansible(self, hosts, task):
        self.ansible.execute(hosts, task)

    def get_container(self, container_id, host=None):
        container = None
        if host is None:
            for node in self.nodes:
                try:
                    container = node.get_container(container_id)
                except Exception as e:
                    continue
                if container:
                    break
            if container is None:
                raise Exception("Container with id=%s not found on any host" % container_id)
        container = self.nodes[host].get_container(container_id)
        return container

    def get_target(self, target):
        if target['type'] == 'container':
            return self.get_container(target['id'], target['host'])
        elif target['type'] == 'node':
            return self.get_node(target['id'])
        else:
            raise Exception("Target type does not exist")

    def unpack_node(self, node_info):
        host = node_info.host
        node_data = node_info.payload
        containers = dict()
        for container_info in node_data['containers']:
            container = self.unpack_container(container_info, host)
            containers[container.id] = container
        node = Node(ip=host, containers=containers, node_info=node_info)
        return node

    def unpack_container(self, container_info, host):
        params = {"host": host, "container_driver": self.cont_d}
        for key, val in container_info.items():
            if key == "Names":
                params['name'] = val[0][1:]
            else:
                params[key.lower()] = val

        container = Container(**params)
        return container

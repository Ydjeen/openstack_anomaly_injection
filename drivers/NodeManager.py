import json
from api.node import Node
from api.container import Container
from drivers.container_driver import DockerContainer
from ansible_runner import AnsibleRunner


class NodeManager:
    def __init__(self, config):
        self._parse_init(config)
        ansibleExecutor = AnsibleRunner({})
        self.container_driver = DockerContainer(ansibleExecutor)

    def _parse_init(self, config):
        self.nodes = self.discover()
        # raise NotImplementedError

    def discover(self):
        config = json.load(open("result.json"))
        nodes = {}
        for node in config:
            node = unpack_node(node)
            nodes[node.ip] = node

        return nodes

    def list_containers(self, host='all'):
        result = {}
        if host == 'all':
            for host, node in self.nodes.items():
                result[host] = node.list_containers()
        else:
            result[host] = self.nodes[host].list_containers()
        return result

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

    def stop_container(self, container_id, host=None):
        container = self.get_container(container_id, host)
        return self.container_driver.stop(container)


def unpack_node(node_info):
    host = node_info[0]
    node_data = node_info[1]
    node_id = node_data["ID"]
    containers = dict()
    for container_info in node_info[2]:
        container = unpack_container(container_info, host)
        containers[container.id] = container
    node = Node(ip=host, id=node_id, containers=containers, node_info=node_info)
    return node


def unpack_container(container_info, host):
    params = {"host": host}
    for key, val in container_info.items():
        if key == "Names":
            params['name'] = val[0][1:]
        else:
            params[key.lower()] = val

    container = Container(**params)
    return container

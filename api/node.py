class Node:
    ATTRS = ('ip', 'auth')

    def __init__(self, ip, id, containers=None, node_info=None):
        self.ip = ip
        self._id = id
        self.containers = containers or {}
        self.node_info = node_info or {}

    def list_containers(self):
        return [(key, cont.name) for key, cont in self.containers.items()]

    def get_container(self, container_id):
        return self.containers[container_id]

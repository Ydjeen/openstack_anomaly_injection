class Node:
    ATTRS = ('ip', 'auth')

    def __init__(self, ip, containers=None, node_info=None):
        self.ip = ip
        self.containers = containers or {}
        self.node_info = node_info or {}

    def list_containers(self):
        return [(key, cont.name) for key, cont in self.containers.items()]

    def get_container(self, container_id):
        full_id = [x for x in self.containers.keys() if container_id in x][0]
        return self.containers[full_id]

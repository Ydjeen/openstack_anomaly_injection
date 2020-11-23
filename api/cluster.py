class Cluster:
    def __init__(self, nodes, cluster_info=None):
        self.nodes = nodes
        self.cluster_info = cluster_info

    @property
    def hosts(self):
        return sorted(self.nodes)

    def __len__(self):
        return len(self.nodes)

    def __getitem__(self, item):
        return self.nodes[item]

    def get_ips(self):
        return [host.ip for host in self.nodes]


class Deployment:
    def __init__(self, nodes, driver, cluster_info=None):
        self.nodes = nodes
        self.driver = driver
        self.cluster_info = cluster_info

    @property
    def hosts(self):
        return sorted(self.nodes)

    def __len__(self):
        return len(self.nodes)

    def __getitem__(self, item):
        return self.nodes[item]

    def get_ips(self):
        return [host for host in self.nodes.keys()]

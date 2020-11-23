class AnsibleRunner:
    def __init__(self, config):
        self.config = config
        pass

    @staticmethod
    def execute(hosts, task):
        print("Executing %s on hosts %s" % (task, hosts))

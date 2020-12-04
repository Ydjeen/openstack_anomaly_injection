from node_control.ansible_runner import AnsibleRunner


class DockerContainer:
    def __init__(self, ansible_runner: AnsibleRunner):
        self.ansible_executor = ansible_runner

    def _run_task(self, hosts, task, msg):
        result = self.ansible_executor.execute(hosts, task)
        if result[0].status == 'OK':
            print("Task", msg, "executed Successfully")
        return result

    def start(self, name, host):
        task = {
            'shell': {
                'cmd': f'docker start {name}'
            },
        }
        nodes = [host]
        self._run_task(nodes, task, 'Start')

    def stop(self, name, host):
        task = {
            'shell': {
                'cmd': f'docker stop {name}'
            },
        }
        nodes = [host]
        self._run_task(nodes, task, 'Stop')

    def terminate(self, name, host):
        task = {
            'shell': {
                'cmd': f'docker kill {name}'
            },
        }
        nodes = [host]
        self._run_task(nodes, task, 'Terminate')

    def restart(self, name, host):
        task = {
            'shell': {
                'cmd': f'docker restart {name}'
            },
        }
        nodes = [host]
        self._run_task(nodes, task, 'Restart')

    def stress(self, name, host, stressors):
        #TODO: how to implement this
        task = {
            'shell': {
                'cmd': f'stress-ng' + stressors
            },
        }
        nodes = [host]
        self._run_task(nodes, task, 'Stress')

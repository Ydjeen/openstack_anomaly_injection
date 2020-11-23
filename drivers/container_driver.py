from ansible_runner import AnsibleRunner


class DockerContainer:
    def __init__(self, ansible_runner):
        self.ansible_executor = ansible_runner

    def _run_task(self, hosts, task, msg):
        self.ansible_executor.execute(hosts, task)

    def start(self, name, host):
        task = {
            'docker_container': {
                'name': name, 'state': 'started'
            },
        }
        nodes = [host]
        self._run_task(nodes, task, 'Start')

    def stop(self, name, host):
        task = {
            'docker_container': {
                'name': name, 'state': 'stopped'
            },
        }
        nodes = [host]
        self._run_task(nodes, task, 'Stop')

    def terminate(self, name, host):
        task = {
            'docker_container': {
                'name': name, 'state': 'stopped'
            },
        }
        nodes = [host]
        self._run_task(nodes, task, 'Terminate')

    def restart(self, name, host):
        task = {
            'docker_container': {
                'name': name, 'state': 'started',
                'restart': 'yes'
            },
        }
        nodes = [host]
        self._run_task(nodes, task, 'Restart')

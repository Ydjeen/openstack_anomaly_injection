from .base_driver import BaseDriver
import logging

log_info = logging.getLogger('infoLog')
log_error = logging.getLogger('errorLog')
log_debug = logging.getLogger('debuggerLog')
log_status = logging.getLogger('statusLog')


class DockerContainer(BaseDriver):
    def start(self, name, host):
        """Start the container."""
        task = {
            'shell': {
                'cmd': f'docker start {name}'
            },
        }
        hosts = [host]
        return self._run_task(hosts, task, 'Start')

    def stop(self, name, host):
        """Stop the container"""

        task = {
            'shell': {
                'cmd': f'docker stop {name}'
            },
        }
        hosts = [host]
        return self._run_task(hosts, task, 'Stop')

    def terminate(self, name, host):
        """Terminate the container"""

        task = {
            'shell': {
                'cmd': f'docker kill {name}'
            },
        }
        hosts = [host]
        return self._run_task(hosts, task, 'Terminate')

    def restart(self, name, host):
        """Restart the container"""

        task = {
            'shell': {
                'cmd': f'docker restart {name}'
            },
        }
        hosts = [host]
        return self._run_task(hosts, task, 'Restart')

    def stress(self, name, host, stressors):
        """Perform stress test on the container using stress-ng. Note: dockhack is used in order to run the stressors on
        the resource group that the containers belongs to.

         :param name: Container name
         :type name: str
         :param host: Hostname
         :type name: str
         :param stressors: stress-ng arguments
         :type stressors: str
         """

        task = {
            'shell': {
                'cmd': f'dockhack cg_exec {name} stress-ng ' + stressors
            },
        }
        hosts = [host]
        return self._run_task(hosts, task, 'Stress')

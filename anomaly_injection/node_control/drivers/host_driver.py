import logging
from .base_driver import BaseDriver

log_info = logging.getLogger('infoLog')
log_error = logging.getLogger('errorLog')
log_debug = logging.getLogger('debuggerLog')
log_status = logging.getLogger('statusLog')


class HostDriver(BaseDriver):
    def start(self, host):
        raise NotImplementedError

    def stop(self, host):
        raise NotImplementedError

    def terminate(self, name, host):
        raise NotImplementedError

    def restart(self, name, host):
        raise NotImplementedError

    def stress(self, host, stressors):
        """Perform stress-test on the host.

         :param host: Hostname
         :type host: str
         :param stressors: stress-ng arguments
         :type stressors: str
         """
        task = {
            'shell': {
                'cmd': f'stress-ng ' + stressors
            },
        }
        hosts = [host]
        self._run_task(hosts, task, 'Stress')

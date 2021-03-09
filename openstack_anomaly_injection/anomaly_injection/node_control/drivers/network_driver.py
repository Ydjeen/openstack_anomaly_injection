from .base_driver import BaseDriver
import logging

log_info = logging.getLogger('infoLog')
log_error = logging.getLogger('errorLog')
log_debug = logging.getLogger('debuggerLog')
log_status = logging.getLogger('statusLog')


class NetworkDriver(BaseDriver):
    def script(self, interface, host, filename):
        """Perform stress test on the container using stress-ng. Note: dockhack is used in order to run the stressors on
        the resource group that the containers belongs to.

         :param interface: Name of network interface
         :type interface: str
         :param host: Hostname
         :type host: str
         :param filename: Path to file on local disk
         :type filename: str
         """

        task = {
            'name': 'Script',
            'raw':  "tcset --delay 100ms lo"

        }
        hosts = [host]
        return self._run_task(hosts, task, 'Script')

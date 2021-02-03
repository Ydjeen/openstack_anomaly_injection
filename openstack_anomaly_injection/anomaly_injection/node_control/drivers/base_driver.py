import logging
from anomaly_injection.node_control.drivers.ansible_runner import AnsibleRunner

log_info = logging.getLogger('infoLog')
log_error = logging.getLogger('errorLog')
log_debug = logging.getLogger('debuggerLog')
log_status = logging.getLogger('statusLog')


class BaseDriver(object):
    """Base driver class. All drivers receive AnsibleRunner objects.

    :ivar ansible_executor: AnsibleRunner object
    :type ansible_executor: :class:`.drivers.ansible_runner.AnsibleRunner`

    :param ansible_runner: AnsibleRunner object
    :type ansible_runner: :class:`.drivers.ansible_runner.AnsibleRunner`
    """

    def __init__(self, ansible_runner: AnsibleRunner):
        self.ansible_executor = ansible_runner

    def _run_task(self, hosts, task, task_name):
        """
        
        :param hosts: Target hosts
        :type hosts: list
        :param task: Ansible-playbook task
        :type task: dic
        :param task_name: Task Name
        :type task_name: str
        :return: 
        """
        log_debug.debug(f"Executing task {task_name} on hosts {', '.join(hosts)}")
        result = self.ansible_executor.execute(hosts, task)
        if result[0].status == 'OK':
            log_debug.debug(f"Task {task_name} executed Successfully")
        return result

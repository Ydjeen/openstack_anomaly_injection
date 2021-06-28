import collections
import json
import logging
import os
import shlex
import tempfile

import yaml
from oslo_concurrency import processutils
from oslo_concurrency.processutils import ProcessExecutionError

STATUS_OK = 'OK'
STATUS_FAILED = 'FAILED'
STATUS_UNREACHABLE = 'UNREACHABLE'
STATUS_SKIPPED = 'SKIPPED'

log_info = logging.getLogger('infoLog')
log_error = logging.getLogger('errorLog')
log_debug = logging.getLogger('debuggerLog')
log_status = logging.getLogger('statusLog')


class AnsibleRunner:
    """Ansible Runner is the interface between the library and the deployment. The library performs ansible tasks in
    order to execute commands. This class builds an ansible playbook file and runs it on a target host.

    :param auth_vars:  Authentication variables for connecting to target host. View cloud_config.json for more info.
    :type auth_vars: dict
    """

    AnsibleExecutionRecord = collections.namedtuple(
        'AnsibleExecutionRecord', ['host', 'status', 'task', 'payload'])

    def __init__(self, auth_vars):
        self.auth_vars = auth_vars

    def _run_play(self, play_source):
        """
        Creates a playbook file and runs it against target hosts.

        :param play_source: Dictionary containing the tasks and the hosts that ansible needs to run on.
        :type play_source: dict

        :returns: Named tuple containing the 'host', 'status', 'task' and 'payload' in json format.
        :rtype: AnsibleExecutionRecord
        """
        full_inventory = {'all': {'hosts': play_source['hosts'], 'vars': self.auth_vars}}

        temp_dir = tempfile.mkdtemp(prefix='temp_files')
        inventory_file_name = f'{temp_dir}/inventory'
        with open(inventory_file_name, 'w') as outfile:
            yaml.dump(full_inventory, outfile, default_flow_style=False)
        playbook_file_name = os.path.join(temp_dir, 'playbook')

        with open(inventory_file_name, 'w') as fd:
            cnt = yaml.safe_dump(full_inventory, default_flow_style=False)
            print(cnt, file=fd)
            log_debug.debug('Inventory:\n%s', cnt)
        play = {
            'hosts': 'all',
            'gather_facts': 'no',
            'become': 'True',
            'tasks': play_source['tasks'],
        }

        with open(playbook_file_name, 'w') as fd:
            cnt = yaml.safe_dump([play], default_flow_style=False)
            print(cnt, file=fd)
            log_debug.debug('Playbook:\n%s', cnt)

        # TODO: this is a workaround
        cmd = ('env ANSIBLE_STDOUT_CALLBACK=json ansible-playbook -i %(inventory)s %(playbook)s' %
               {'inventory': inventory_file_name,
                'playbook': playbook_file_name})

        print(cmd)
        logging.info('Executing %s' % cmd)
        try:
            command_stdout, command_stderr = processutils.execute(
                *shlex.split(cmd))
        except ProcessExecutionError as err:
            command_stdout, command_stderr = err.stdout, err.stderr

        d = json.loads(command_stdout[command_stdout.find('{'):])
        h = d['plays'][0]['tasks'][0]['hosts']
        recs = []
        for h, hv in h.items():
            if hv.get('unreachable'):
                status = STATUS_UNREACHABLE
                raise Exception("Host %s is %s" % (h, status))
            elif hv.get('failed'):
                status = STATUS_FAILED
                _task_name = play_source.get("tasks", [{}])[0].get("name", "")
                sout = hv.get('stdout', "")
                _reason = sout if len(sout) > 0 else hv.get("stderr", "")
                raise Exception(f"Task %s has %s due to: %s" % (_task_name, status, _reason))
            else:
                status = STATUS_OK

            r = self.AnsibleExecutionRecord(host=h, status=status, task='',
                                            payload=hv)
            recs.append(r)

        return recs

    def _run_playbook(self, playbook):
        result = []

        for play_source in playbook:
            play_source['gather_facts'] = 'no'

            result += self._run_play(play_source)

        return result

    def execute(self, hosts, task, task_name=""):
        """
        Execute a task on target hosts

        :param hosts:  List of hosts
        :type hosts: list

        :param task:  Task that needs to be executed
        :type task: dict

        :returns: List of Named tuples containing the 'host', 'status', 'task' and 'payload' in json format.
        :rtype: list
        """
        hosts_dictionary = {}
        for host in hosts:
            hosts_dictionary[host] = []
        task_play = {'hosts': hosts_dictionary,
                     'tasks': [task]}
        return self._run_playbook([task_play])

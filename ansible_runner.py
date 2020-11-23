import collections
import json
import logging
import os
import tempfile
import shlex

import yaml
from oslo_concurrency import processutils

from openstack_discovery import AnsibleExecutionRecord

STATUS_OK = 'OK'
STATUS_FAILED = 'FAILED'
STATUS_UNREACHABLE = 'UNREACHABLE'
STATUS_SKIPPED = 'SKIPPED'

LOG = logging.getLogger(__name__)

class AnsibleRunner:


    AnsibleExecutionRecord = collections.namedtuple(
        'AnsibleExecutionRecord', ['host', 'status', 'task', 'payload'])

    def __init__(self, config):
        self.config = config
        pass

    def _run_play(self, auth_vars, play_source):
        inventory = {}
        full_inventory = {'all': {'hosts': play_source['hosts'], 'vars': auth_vars}}

        temp_dir = tempfile.mkdtemp(prefix='temp_files')
        inventory_file_name = f'{temp_dir}/inventory'
        with open(inventory_file_name, 'w') as outfile:
            yaml.dump(full_inventory, outfile, default_flow_style=False)
        playbook_file_name = os.path.join(temp_dir, 'playbook')

        with open(inventory_file_name, 'w') as fd:
            cnt = yaml.safe_dump(full_inventory, default_flow_style=False)
            print(cnt, file=fd)
            LOG.debug('Inventory:\n%s', cnt)

        play = {
            'hosts': 'all',
            'gather_facts': 'no',
            'become': 'True',
            'tasks': play_source['tasks'],
        }

        with open(playbook_file_name, 'w') as fd:
            cnt = yaml.safe_dump([play], default_flow_style=False)
            print(cnt, file=fd)
            LOG.debug('Playbook:\n%s', cnt)

        cmd = ('ansible-playbook -i %(inventory)s %(playbook)s' %
               {'inventory': inventory_file_name,
                'playbook': playbook_file_name})

        logging.info('Executing %s' % cmd)
        command_stdout, command_stderr = processutils.execute(
            *shlex.split(cmd),
            env_variables={'ANSIBLE_STDOUT_CALLBACK': 'json'},
            check_exit_code=False)

        d = json.loads(command_stdout[command_stdout.find('{'):])
        h = d['plays'][0]['tasks'][0]['hosts']
        recs = []
        for h, hv in h.items():
            if hv.get('unreachable'):
                status = STATUS_UNREACHABLE
            elif hv.get('failed'):
                status = STATUS_FAILED
            else:
                status = STATUS_OK
            r = AnsibleExecutionRecord(host=h, status=status, task='',
                                       payload=hv)
            recs.append(r)

        return recs

    def _run_playbook(self, auth_vars, playbook):
        result = []

        for play_source in playbook:
            play_source['gather_facts'] = 'no'

            result += self._run_play(auth_vars, play_source)

        return result

    def execute(self, hosts, task):
        hosts_dictionary = {}
        for host in hosts:
            hosts_dictionary[host] = []
        task_play = {'hosts': hosts_dictionary,
                     'tasks': [task]}
        return self._run_playbook(self.config, [task_play])

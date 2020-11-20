import collections
import json
import logging
import os
import subprocess
import tempfile
import shlex

import yaml

import ansible_runner

from oslo_concurrency import processutils

LOG = logging.getLogger(__name__)

STATUS_OK = 'OK'
STATUS_FAILED = 'FAILED'
STATUS_UNREACHABLE = 'UNREACHABLE'
STATUS_SKIPPED = 'SKIPPED'

AnsibleExecutionRecord = collections.namedtuple(
    'AnsibleExecutionRecord', ['host', 'status', 'task', 'payload'])

#depreciated
def discover_containers():
    bootstrap_ansible_cmd = ["ansible-playbook",
                             "--inventory", "inventory",
                             "discover_containers.yaml"]
    output = None
    try:
        output = subprocess.run(bootstrap_ansible_cmd, capture_output=True)
    except subprocess.CalledProcessError as e:
        logging.error("Pre-bootstrapping failed. Error code: {}. "
                      "Error message {}", e.returncode, e.output)
    if output:
        print(output)
        with open('container_list', 'r') as outfile:
            data = json.load(outfile)
            print(data)

def discover_containers_ansible_runner():
    r = ansible_runner.run(private_data_dir='./', playbook='discover_containers.yaml',
                           inventory='inventory', json_mode=True)
    result = list()
    for event in r.events:
        try:
            if event['event_data']['res']['containers']:
                result.append((event['event_data']['host'],
                               event['event_data']['res']['host_info'],
                               event['event_data']['res']['containers']))
        except KeyError:
            pass
    return (result)

def execute_task(hosts, task):
    task_play = {'hosts': hosts,
                 'tasks': [task]}
    result = run_playbook([task_play])

def run_playbook(playbook):
    result = []

    for play_source in playbook:
        play_source['gather_facts'] = 'no'

        result += _run_play(play_source)

    return result

def _run_play(play_source):
    inventory = {}

    auth_vars = {'ansible_user': 'yevhen', 'ansible_private_key_file': '~/.ssh/id_rsa'}

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

def info_task():
    task = {
        'docker_host_info': {
            'containers': 'yes'
        },
    }
    return task

default_hosts = {"wally098.cit.tu-berlin.de":[], "wally099.cit.tu-berlin.de":[]}
print (execute_task(default_hosts, info_task()))
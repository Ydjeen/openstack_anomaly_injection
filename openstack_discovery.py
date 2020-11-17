import json
import logging
import subprocess

import ansible_runner

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

print (discover_containers_ansible_runner())
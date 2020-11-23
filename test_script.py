from drivers.NodeManager import NodeManager

config = {'ansible_user': 'pilijevski', 'ansible_private_key_file': '~/.ssh/id_rsa'}

manager = NodeManager(config)
print(manager.list_containers())

print(manager.stop_container("352eb13ca0d36af3c5c84fe2aff7da915de366c52763fa9f77cb56cdc14f0ca8",
                             "wally098.cit.tu-berlin.de"))

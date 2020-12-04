from node_control.cloud_management import CloudManagement
import json

config = json.load(open("../cloud_config.json"))

conn = CloudManagement(config)
cloud = conn.cluster

# conn.connect()
# conn.verify()
#
# print(conn.list_containers())
# print(conn.get_container("352eb13ca0d36af3c5c84fe2aff7da915de366c52763fa9f77cb56cdc14f0ca8",
#                              "wally098.cit.tu-berlin.de"))
#

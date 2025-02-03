### Prerequisite

Python 3.9+


### Example
```
import json
from scpapi import Client
from scpapi.resource.virtual_server import VirtualServer


### First create a client with your credentials ###
client = Client(
    project_id='PROJECT-XXXXXXXXXX',
    access_key='XXXXXXXXXX',
    secret_key='XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
)
### Create a virtual server with created client ###
virtual_server = VirtualServer(client=client)

### List of Virtual Server ###
vm_list = json.loads(virtual_server.list().text)
print(vm_list['contents'])

### Create a Virtual Server ###
virtual_server_body = {
    'virtualServerName': 'slurm-head',
    'blockStorage': {
        'blockStorageName': 'root',
        'diskSize': 100,
        'encryptEnabled': False,
        'diskType': 'SSD'
    },
    'imageId': 'IMAGE-XXXXXXXXXXXXXXXXXXXX',
    'nic': {
        'subnetId': 'SUBNET-XXXXXXXXXXXXXXXXXXXX',
        'natEnabled': True,
        'publicIpId' : 'PUBLIC_IP-XXXXXXXXXXXXXXXXXXXX'
    },
    'deletionProtectionEnabled': False,
    'securityGroupIds': ['FIREWALL_SECURITY_GROUP-XXXXXXXXXX'],
    'serverType': 's1v2m4',
    'serviceZoneId': 'ZONE-XXXXXXXXXXXXXXXXXXXX',
    'serverGroupId': 'SERVICE-XXXXXXXXXXXXXXXXXXXX',
    'tags': [
        {'tagKey': 'cluster-name', 'tagValue': 'slurm-cluster'},
    ],
    'keyPairId': 'KEY_PAIR-XXXXXXXXXXXXXXXXXXXX'
}

print(virtual_server.create(body=virtual_server_body).text)
```
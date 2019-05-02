from nagini import Nagini, NaginiException
import argparse

# See requirements folder in the root of this repository for details
# for installing the Nagini module

parser = argparse.ArgumentParser(description='VROPS API example')
parser.add_argument('-H', help='VROPS to connect to', nargs=1, required=True)
parser.add_argument('-u', help='VROPS User to connect as', nargs=1, required=True)
parser.add_argument('-p',
                    help='VROPS User password to connect with.' +
                    ' If unspecified the script will use a default.',
                    nargs=1, required=True)
group = parser.add_mutually_exclusive_group()
group.add_argument('-c', help='VMware cluster name', nargs=1)
group.add_argument('-l', help='List VMware clusters', action='store_true')

username = vars(parser.parse_args())['u'][0]
password = vars(parser.parse_args())['p']

if not vars(parser.parse_args())['H']:
    host = raw_input('Enter VROPS host: ')
else:
    host = vars(parser.parse_args())['H'][0]


client = Nagini(host=host, user_pass=[username, password])

if vars(parser.parse_args())['l']:
    for cluster in client.get_resources(resourceKind="ClusterComputeResource")['resourceList']:
        print(cluster['resourceKey']['name'])
    exit(0)

if vars(parser.parse_args())['c']:
    status = str(client.get_resources(resourceKind="ClusterComputeResource",name=vars(parser.parse_args())['c'][0])['resourceList'][0]['resourceHealth'])
    if status == "GREEN":
        print("Cluster is healthy")
        exit(0)
    if status == "YELLOW":
        print("Cluster is degraded")
        exit(1)
    if status == "GREY":
        print("Cluster is degraded")
        exit(1)
    if status == "ORANGE":
        print("Cluster is degraded")
        exit(1)
    if status == "RED":
        print("Cluster is down")
        exit(2)

print(status)
print("Unknown problem")
exit(3)

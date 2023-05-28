from Node64Client import Node64Client
from os import geteuid, getenv
import sys

nodeColor = False # Default Disable
if str(getenv('Node64Color')).lower() == "true":
    nodeColor=True

if len(sys.argv) == 2:
    nodeSecret = sys.argv[1]
elif getenv('Node64Secret'):
    nodeSecret = getenv('Node64Secret')
else:
    print(f"{sys.argv[0]} <your node secret>")
    sys.exit(1)
    

if __name__ == "__main__":
    if geteuid() != 0:
        exit("You need to have root privileges to run this script.\nPlease try again, this time using 'sudo'. Exiting.")
    else:
        client = Node64Client(nodeSecret,nodeColor)
        client.run()

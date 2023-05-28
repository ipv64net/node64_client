from Node64Client import Node64Client
from os import geteuid, getenv
import sys

if getenv('Node64Secret'):
    node_secret = getenv('Node64Secret')
elif len(sys.argv) == 1:
    print(f"{sys.argv[0]} <your node secret>")
    sys.exit(1)
else:
    node_secret = sys.argv[1]


if __name__ == "__main__":
    if geteuid() != 0:
        exit("You need to have root privileges to run this script.\nPlease try again, this time using 'sudo'. Exiting.")
    else:
        client = Node64Client(node_secret)
        client.run()

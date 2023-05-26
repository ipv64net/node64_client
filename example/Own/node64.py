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

class myclient(Node64Client):
    def stats(self,_,task,result,response,runtime):
        print(f"task {task}")
        print(f"result {result}")
        print(f"response {response}")
        print(f"runtime {runtime}")

if __name__ == "__main__":
    if geteuid() != 0:
        exit("You need to have root privileges to run this script.\nPlease try again, this time using 'sudo'. Exiting.")
    else:
        client = myclient(node_secret)
        client.run()

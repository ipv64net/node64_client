from Node64Client import Node64Client
from os import getenv, name as osname
import sys
import time
import threading

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


StopServer = False

def runserver():
    t = threading.current_thread()
    while getattr(t, "do_run", True):
        time.sleep(10)
        print("Hello from Server")
    print("Server Stop")

class myclient(Node64Client):
    def stats(self,_,task,result,response,runtime):
        print(f"task {task}")
        print(f"result {result}")
        print(f"response {response}")
        print(f"runtime {runtime}")

if __name__ == "__main__":
    if osname != 'nt':
        from os import geteuid
        if geteuid() != 0:
            exit("You need to have root privileges to run this script.\nPlease try again, this time using 'sudo'. Exiting.")
    else:
        threadserver = threading.Thread(target=runserver)
        threadserver.start()
        client = myclient(nodeSecret,nodeColor)
        client.run()
        threadserver.do_run = False

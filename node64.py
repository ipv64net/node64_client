from Node64Client import Node64Client
from os import geteuid


class myclient(Node64Client):
    def stats(self,task,result,response,runtime):
        print(f"task {task}")
        print(f"result {result}")
        print(f"response {response}")
        print(f"runtime {runtime}")

if __name__ == "__main__":
    if geteuid() != 0:
        exit("You need to have root privileges to run this script.\nPlease try again, this time using 'sudo'. Exiting.")
    else:
        client = myclient('')
        client.run()

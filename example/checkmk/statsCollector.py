
import sys
from os import getenv, name as osname, path

__REALAPPPATH__ = path.dirname(path.dirname(path.dirname(path.realpath(__file__))))
sys.path.append(__REALAPPPATH__)

from Node64Client import Node64Client

import sqlite3
import json

class statsCollector(Node64Client):

    def __init__(self, SecretKey, colorOutput=False):
        super().__init__(SecretKey, colorOutput)
        self.sqlinit()

    def sqlinit(self):
        self.con = sqlite3.connect(f"{__REALAPPPATH__}/stats/stats.db",10)
        self.con.execute('CREATE TABLE IF NOT EXISTS tasks (id CHAR PRIMARY KEY, field CHAR, successful INT, runtime REAL, dt datetime default current_timestamp);')
        self.con.commit()
        self.con.close()

    def sqlwrite(self,task,result,runtime):
        self.con = sqlite3.connect(f"{__REALAPPPATH__}/stats/stats.db",10)
        taskresult = 1
        result = json.loads(result)

        if 'error' in result:
            if not result['error'] in {'0','no'}:
                taskresult = 0
        elif 'error_msg' in result:
            if not result['error_msg'] in {'0','no'}:
                taskresult = 0

        self.con.execute(f"INSERT INTO tasks VALUES ('{task['task_id']}', '{task['task_type']}', {taskresult}, {runtime}, current_timestamp)")
        self.con.commit()
        self.con.close()

    def stats(self,task,result,response,runtime):     
        self.sqlwrite(task,result,runtime)

if __name__ == "__main__":
    if osname != 'nt':
        from os import geteuid
        if geteuid() != 0:
            exit("You need to have root privileges to run this script.\nPlease try again, this time using 'sudo'. Exiting.")

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
    client = statsCollector(nodeSecret,nodeColor)
    client.MaxWait = 16
    client.run()
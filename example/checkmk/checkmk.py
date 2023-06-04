import statsCollector
from os import getenv, name as osname, path, makedirs
__REALAPPPATH__ = path.dirname(path.dirname(path.dirname(path.realpath(__file__))))

import sys
import time
import threading
from socketserver import TCPServer,StreamRequestHandler
import sqlite3

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
ScriptVersion = ''

def runserver():
    t = threading.current_thread()
    while getattr(t, "do_run", True):
        time.sleep(10)
        print("Hello from Server")
    print("Server Stop")

class checkmk_checker(object):

    def do_checks(self,**kwargs):
        global ScriptVersion
        _lines = ["<<<check_mk>>>"]
        _lines.append("AgentOS: node64")
        _lines.append(f"Version: {ScriptVersion}")
        _lines.append("Hostname: node64")

        con = sqlite3.connect(f"{__REALAPPPATH__}/stats/stats.db")
        fields = con.execute("SELECT field from tasks GROUP by field ORDER BY field ASC")
        fieldnames = [field[0] for field in fields]

        Stats = {}
        Stats['global'] = { 'total': {'count':0, 'runtime':0, 'successful':0, 'failed':0},
                            'today': {'count':0, 'runtime':0, 'successful':0, 'failed':0},
                            '24h': {'count':0, 'runtime':0, 'successful':0, 'failed':0}}
        Stats['fields'] = {}

        for field in fieldnames:
            Stats['fields'].update({ field: {'total': {'count':0, 'runtime':0, 'successful':0, 'failed':0},
                            'today': {'count':0, 'runtime':0, 'successful':0, 'failed':0},
                            '24h': {'count':0, 'runtime':0, 'successful':0, 'failed':0}}})
            sql = f"SELECT count(*) as count, IFNULL(SUM(runtime),0) as runtime, IFNULL(SUM(successful),0) as successful from tasks WHERE field = '{field}';"
            results = con.execute(sql)
            data = results.fetchone()
            Stats['global']['total']['count'] += int(data[0])
            Stats['global']['total']['runtime'] += round(float(data[1]),2)
            Stats['global']['total']['successful'] += int(data[2])
            Stats['global']['total']['failed'] = Stats['global']['total']['count']-Stats['global']['total']['successful']

            Stats['fields'][field]['total']['count'] += int(data[0])
            Stats['fields'][field]['total']['runtime'] += round(float(data[1]),2)
            Stats['fields'][field]['total']['successful'] += int(data[2])
            Stats['fields'][field]['total']['failed'] = Stats['fields'][field]['total']['count']-Stats['fields'][field]['total']['successful']

            sql = f"SELECT count(*) as count, IFNULL(SUM(runtime),0) as runtime, IFNULL(SUM(successful),0) as successful from tasks WHERE field = '{field}' and dt >= datetime('now','-24 hours');"
            results = con.execute(sql)
            data = results.fetchone()
            Stats['global']['today']['count'] = int(data[0])
            Stats['global']['today']['runtime'] = round(float(data[1]),2)
            Stats['global']['today']['successful'] = int(data[2])
            Stats['global']['today']['failed'] = Stats['global']['today']['count']-Stats['global']['today']['successful']

            Stats['fields'][field]['today']['count'] = int(data[0])
            Stats['fields'][field]['today']['runtime'] = round(float(data[1]),2)
            Stats['fields'][field]['today']['successful'] = int(data[2])
            Stats['fields'][field]['today']['failed'] = Stats['fields'][field]['today']['count']-Stats['fields'][field]['today']['successful']

            sql = f"SELECT count(*) as count, IFNULL(SUM(runtime),0) as runtime, IFNULL(SUM(successful),0) from tasks WHERE field = '{field}' and date(dt) = date('now');"
            results = con.execute(sql)
            data = results.fetchone()
            Stats['global']['24h']['count'] = int(data[0])
            Stats['global']['24h']['runtime'] = round(float(data[1]),2)
            Stats['global']['24h']['successful'] = int(data[2])
            Stats['global']['24h']['failed'] = Stats['global']['24h']['count']-Stats['global']['24h']['successful']

            Stats['fields'][field]['24h']['count'] = int(data[0])
            Stats['fields'][field]['24h']['runtime'] = round(float(data[1]),2)
            Stats['fields'][field]['24h']['successful'] = int(data[2])
            Stats['fields'][field]['24h']['failed'] = Stats['fields'][field]['24h']['count']-Stats['fields'][field]['24h']['successful']

        _lines.append("<<<local:sep(0)>>>")
        count=f'total_count={Stats["global"]["total"]["count"]}|today_count={Stats["global"]["today"]["count"]}|24h_count={Stats["global"]["24h"]["count"]}'
        runtime=f'total_runtime={Stats["global"]["total"]["runtime"]}|today_runtime={Stats["global"]["today"]["runtime"]}|24h_runtime={Stats["global"]["24h"]["runtime"]}'
        successful=f'total_successful={Stats["global"]["total"]["successful"]}|today_successful={Stats["global"]["today"]["successful"]}|24h_successful={Stats["global"]["24h"]["successful"]}'
        failed=f'total_failed={Stats["global"]["total"]["failed"]}|today_failed={Stats["global"]["today"]["failed"]}|24h_failed={Stats["global"]["24h"]["failed"]}'
        _lines.append(f'0 "Tasks" {count}|{runtime}|{successful}|{failed} Summary')
        for field in Stats['fields'].keys():
            count=f'total_count={Stats["fields"][field]["total"]["count"]}|today_count={Stats["fields"][field]["today"]["count"]}|24h_count={Stats["fields"][field]["24h"]["count"]}'
            runtime=f'total_runtime={Stats["fields"][field]["total"]["runtime"]}|today_runtime={Stats["fields"][field]["today"]["runtime"]}|24h_runtime={Stats["fields"][field]["24h"]["runtime"]}'
            successful=f'total_successful={Stats["fields"][field]["total"]["successful"]}|today_successful={Stats["fields"][field]["today"]["successful"]}|24h_successful={Stats["fields"][field]["24h"]["successful"]}'
            failed=f'total_failed={Stats["fields"][field]["total"]["failed"]}|today_failed={Stats["fields"][field]["today"]["failed"]}|24h_failed={Stats["fields"][field]["24h"]["failed"]}'
            _lines.append(f'0 "Task {field}" {count}|{runtime}|{successful}|{failed} Summary')

        con.close()
        return "\n".join(_lines).encode("utf-8")

class checkmkHandler(StreamRequestHandler):
    def handle(self):
        try:
            _msg = checkmk_checker.do_checks(self)
        except Exception as e:
            raise
            _msg = str(e).encode("utf-8")
        try:
            self.wfile.write(_msg)
        except:
            pass

def runserver():
    TCPServer.allow_reuse_address = True
    aServer = TCPServer(('', 6556), checkmkHandler)
    aServer.serve_forever()

if __name__ == "__main__":
    if osname != 'nt':
        from os import geteuid
        if geteuid() != 0:
            exit("You need to have root privileges to run this script.\nPlease try again, this time using 'sudo'. Exiting.")

    isExist = path.exists(f"{__REALAPPPATH__}/stats")
    if not isExist:
        makedirs(f"{__REALAPPPATH__}/stats")

    threadserver = threading.Thread(target=runserver)
    threadserver.start()
    client = statsCollector.statsCollector(nodeSecret,nodeColor)
    if getenv('Node64MaxWait'):
        client.MaxWait = int(getenv('Node64MaxWait'))
    ScriptVersion = client.Version
    client.run()
    threadserver.do_run = False


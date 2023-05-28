#!/usr/bin/python3

# import libs

from icmplib import ping, traceroute
from requests import post as httppost
import json
from dns.resolver import Resolver
import signal
import hashlib
import time
import urllib3
import sys
import ipwhois

#Hide verification message
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)



class Node64Client:
    SecretKey = ''
    BaseURL = 'https://ipv64.net/dims/'
    GetTaskURL = BaseURL + 'get_task.php'
    ReportURL = BaseURL + 'report_node_status.php'
    ResultURL = BaseURL + 'task_report_result.php'
    Timeout = 5
    DefaultWait = 60
    Version = "0.0.6"
    signal_exit = False
    _task = ''
    _debug = 0
    _sleep = False

    #Shell Colors
    CINFO = '\033[95m'      # Light Magenta
    CDEBUG = '\033[96m'     # Light Cyan
    COK = '\033[92m'        # Light Green
    CWARNING = '\033[93m'   # Light Yellow
    CERROR = '\033[91m'     # Light Red
    ENDC = '\033[0m'        # Stop Color


    def __init__(self,SecretKey,colorOutput = False):
        self.SecretKey = SecretKey
        self.colorOutput = colorOutput
        self.printInfo(f"SecretKey: {self.SecretKey}")
        self.report_ipv4()
        self.report_ipv6()
        self.report_version()
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)

    def signal_handler(self,sig, frame):
        if sig == signal.SIGINT:
            if not self.signal_exit and not self._sleep:
                self.printWarn('\nYou pressed Ctrl+C!\nTry Exit Programm...\nOr press again to force Exit!')
            else:
                self.printWarn('\nYou pressed Ctrl+C again!\nExit Programm')
                sys.exit(0)
        if sig == signal.SIGTERM:
            self.printNormal('\nExit Programm')
            sys.exit(0)
        self.signal_exit = True

    def printDebug(self,msg):
        if self._debug:
            if self.colorOutput:
                print(f'{self.CDEBUG}{msg}{self.ENDC}')
            else: 
                print(f'{msg}')

    def printNormal(self,msg):
        if self.colorOutput:
            print(f'{self.COK}{msg}{self.ENDC}')
        else: 
            print(f'{msg}')

    def printInfo(self,msg):
        if self.colorOutput:
            print(f'{self.CINFO}{msg}{self.ENDC}')
        else: 
            print(f'{msg}')

    def printWarn(self,msg):
        if self.colorOutput:
            print(f'{self.CWARNING}{msg}{self.ENDC}')
        else: 
            print(f'{msg}')

    def printError(self,msg):
        if self.colorOutput:
            print(f'{self.CERROR}{msg}{self.ENDC}')
        else: 
            print(f'{msg}')

    def sendData(self,url,data):
        http = 0
        try:
            http = httppost(url, data = data, verify=False, timeout=self.Timeout)
            return http
        except:
            if hasattr(http,'status_code'):
                return {"error": http.status_code, "wait": self.DefaultWait , "verbose": 1}
            return {"error": 408, "wait": self.DefaultWait , "verbose": 1}
        
    def getTask(self):
        try:
            result = self.sendData(self.GetTaskURL,{'node_secret': self.SecretKey})
            if result.content:
                return result.json()
            if self._debug:
                self.printError(f"Error sendData {result}")
            return {"error": 42, "wait": self.DefaultWait , "verbose": 1}
        except:
            return {"error": 43, "wait": self.DefaultWait , "verbose": 1}

    def report_version(self):
        self.sendData(self.ReportURL,{'node_secret' : self.SecretKey,'version':self.Version})

    def report_ipv4(self):
        url = 'https://ipv4.ipv64.net/dims/report_node_status.php'
        self.sendData(url,{'node_secret' : self.SecretKey})

    def report_ipv6(self):
        url = 'https://ipv6.ipv64.net/dims/report_node_status.php'
        self.sendData(url,{'node_secret' : self.SecretKey})

    def sendResult(self,task,result):
        if result is not None:
            task_hash = json.dumps({'task':task,'task_result':json.loads(result)})
            myobj = {'node_secret': self.SecretKey,
                     'task_id': task["task_id"],
                     'task_result': result,
                     'task_hash': hashlib.sha256(task_hash.encode('utf-8')).hexdigest()}
            return self.sendData(self.ResultURL,myobj)

    def icmp(self,task,family):
        packet_loss = "0"
        try:
            result = ping(task["icmp_dst"],
                          count=task["icmp_count"], 
                          interval=task["icmp_interval"], 
                          timeout=task["icmp_timeout"], 
                          payload_size=task["icmp_size"], 
                          family=family)
            return json.dumps({"rtt_avg":result.avg_rtt,"rtt_min":result.min_rtt,"rtt_max":result.max_rtt,"packet_loss":result.packet_loss,"jitter":result.jitter,"error_msg":"0"})
        except:
            return json.dumps({"error_msg":"timeout","packet_loss":packet_loss})

    def traceroute(self,task):
        try:
            hops = traceroute(task["trace_dst"],
                              count=task["trace_count"],
                              interval=task["trace_interval"],
                              timeout=task["trace_timeout"],
                              max_hops=task["trace_max_hops"],
                              family=task["trace_family"],
                              payload_size=task["trace_size"])
            last_distance = dist = end_hops = 0
            result = []
            for hop in hops:
                dist += 1
                if last_distance + 1 != hop.distance:
                    task_result = {"distance":dist}
                else:
                    task_result = {"distance":hop.distance,"address":hop.address,"rtt_avg":hop.avg_rtt,"packet_loss":hop.packet_loss,"jitter":hop.jitter,"is_alive":hop.is_alive,"error_msg":"0",}
                result.append(task_result)
                last_distance = hop.distance
            end_hops = {"hops":last_distance}
            result.append(end_hops)
        except:
            result = {"error_msg":"timeout","packet_loss":"1"}
        return json.dumps(result)

    def dns(self,task):
        res = Resolver()
        try:
            result = res.resolve(task["dns_query"],task["dns_type"])
            response_time = round(result.response.time * 100,4)
            records = []
            for IPval in result:
                records.append(IPval.to_text())
            result = {"rrset":records,"latency":response_time,"error":"no"}
        except Exception as err:
            if self._debug:
                self.printError(f"Unexpected {err=}, {type(err)=}")
            result = {"error":"Could not be resolved"}
        return json.dumps(result)
        
    def nslookup(self,task):
        res = Resolver()
        try:
            result = []
            for res in res.resolve_address(task['ns_ip']):
                result = {"ptr":str(res),"ptr_ip":str(task['ns_ip']),"error":"0"}
        except Exception as err:
            if self._debug: 
                self.printError(f"Unexpected {err=}, {type(err)=}")
            result = {"error":"Could not be resolved"}
        return json.dumps(result)

    def whois(self,task):
        try:
            obj = ipwhois.IPWhois(task["whois_dst"],5)
            results = obj.lookup_rdap()
            task_result = {
                    'query': results['query'],
                    'asn_description': results['asn_description'],
                    'asn_cidr': results['asn_cidr'],
                    'asn': results['asn'],
                    'handle': results['network']['handle'],
                    'name': results['network']['name'],
                    'address': results['objects'][results['entities'][0]]['contact']['address'][0]['value']
            }
            return json.dumps(task_result)
        except:
            return json.dumps({"error_msg":"timeout"})

    def runtask(self,tasks):
        for task in tasks:
            result = None
            try:
                self.printNormal(f"Run Task ID: {task['task_id']} Type: {task['task_type']}")
                self.printDebug(f"\tTaskinfo: {task['task_infos']}")
                start_time = time.time()
                # scheiss python syntaxcheck will kein match daher if + elifs
                if task['task_type'] == 'icmpv4':
                    result = self.icmp(task['task_infos'], 4) 
                elif task['task_type'] == 'icmpv6':
                    result = self.icmp(task['task_infos'], 6) 
                elif task['task_type'] == 'traceroute':
                    result = self.traceroute(task['task_infos']) 
                elif task['task_type'] == 'dns':
                    result = self.dns(task['task_infos']) 
                elif task['task_type'] == 'nslookup':
                    result = self.nslookup(task['task_infos']) 
                elif task['task_type'] == 'whois':
                    result = self.whois(task['task_infos']) 
                elif self._debug: 
                    self.printError(f"ERROR: {task['task_type']} unknow")
                    self.printError(f"task data: {task}")

                if result:
                    if self._debug: 
                        self.printDebug(f"\tSend result: {result}")
                    self.printNormal(f"Finished Task {task['task_id']} in {round(time.time() - start_time,4)} seconds")
                    response = self.sendResult(task,result)
                    if hasattr(response, "status_code") and response.status_code != 200: 
                        self.printDebug(f"\tAnswer: {response.status_code} {response.content.decode()}")
                    self.stats(task,result,response,round(time.time() - start_time,4))
            except Exception as err:
                if self._debug:
                    self.printError(f"Unexpected {err=}, {type(err)=}")
    
    def run(self):
        while not self.signal_exit:
            self._task = self.getTask()
            #print(self._task)

            if self._task['error'] > 0: 
                self.printError(f"ipv64 report a {self._task['error']} errorcode")
            else:
                self._debug = int(self._task['verbose'])
                self.runtask(self._task['tasks'])
            if self.signal_exit:
                return

            self._sleep = True
            time.sleep(self._task['wait'] if 'wait' in self._task and self._task['wait'] > 0 else self.DefaultWait)
            self._sleep = False

    def stats(self,task,result,response,runtime):
        pass
        


if __name__ == "__main__":
    exit("This is only a module")

        

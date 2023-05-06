# import libs
import requests
import time
import sys
import urllib3
import signal
import os

# import project modules
import functions

# setting signal handler
signal.signal(signal.SIGINT, functions.signal_handler)
signal.signal(signal.SIGTERM, functions.signal_handler)


#Hide verification message
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

if os.getenv('ipv64NodeSecret'):
    node_secret = os.getenv('ipv64NodeSecret')
elif len(sys.argv) == 1:
    print(f"{sys.argv[0]} <your node secret>")
    sys.exit(1)
else:
    node_secret = sys.argv[1]

print("IPv64.net - Initialisierung")
print(f"using node_secret ${node_secret}")
# At Start, report IPv4 and IPv6
functions.report_ipv4(node_secret)
functions.report_ipv6(node_secret)
functions.report_version(node_secret)

while True:
    url = 'https://ipv64.net/dims/get_task.php'
    myobj = {'node_secret': node_secret}
    
    x = requests.post(url, data=myobj, verify=False)
    x = x.json()
    if x["exit"] == 1:
        sys.exit("Script stopped by IPv64 Master")
    if x["verbose"] == 1:
        print(x)
    if x["error"] > 0:
        print("Error Code:"+ str(x["error"]))
        break
    if x["report_ip"] == 1:
        functions.report_ipv4(node_secret)
        functions.report_ipv6(node_secret)
        print("Report IPv4 & IPv6")
    if 'tasks' in x:
        for _tasks in x["tasks"]:
            task_result = None
            if _tasks["task_type"] == "icmpv4":
                print("Start ICMPv4 Task ID: " + _tasks["task_id"])
                icmp_dst = _tasks["task_infos"]["icmp_dst"]
                icmp_size = _tasks["task_infos"]["icmp_size"]
                icmp_count = _tasks["task_infos"]["icmp_count"]
                icmp_interval = _tasks["task_infos"]["icmp_interval"]
                icmp_timeout = _tasks["task_infos"]["icmp_timeout"]
                task_result = functions.icmp(icmp_dst, icmp_size, icmp_count, icmp_interval, icmp_timeout, 4)
                print("End ICMPv4 Task ID: " + _tasks["task_id"])

            if _tasks["task_type"] == "icmpv6":
                print("Start ICMPv6 Task ID: " + _tasks["task_id"])
                icmp_dst = _tasks["task_infos"]["icmp_dst"]
                icmp_size = _tasks["task_infos"]["icmp_size"]
                icmp_count = _tasks["task_infos"]["icmp_count"]
                icmp_interval = _tasks["task_infos"]["icmp_interval"]
                icmp_timeout = _tasks["task_infos"]["icmp_timeout"]
                task_result = functions.icmp(icmp_dst, icmp_size, icmp_count, icmp_interval, icmp_timeout, 6)
                print("End ICMPv6 Task ID: " + _tasks["task_id"])
                               
            if _tasks["task_type"] == "traceroute":
                print("Start Traceroute Task ID: " + _tasks["task_id"])
                trace_dst = _tasks["task_infos"]["trace_dst"]
                trace_size = _tasks["task_infos"]["trace_size"]
                trace_count = _tasks["task_infos"]["trace_count"]
                trace_interval = _tasks["task_infos"]["trace_interval"]
                trace_timeout = _tasks["task_infos"]["trace_timeout"]
                trace_max_hops = _tasks["task_infos"]["trace_max_hops"]
                trace_family = _tasks["task_infos"]["trace_family"]
                task_result = functions.trace(trace_dst,trace_count,trace_interval,trace_timeout,trace_max_hops,trace_family,trace_size)
                print("End Traceroute Task ID: " + _tasks["task_id"])

            if _tasks["task_type"] == "dns":
                print("Start DNS Task ID: " + _tasks["task_id"])
                dns_query = _tasks["task_infos"]["dns_query"]
                dns_type = _tasks["task_infos"]["dns_type"]
                task_result = functions.dns_resolve(dns_query, dns_type)
                print("End DNS Task ID: " + _tasks["task_id"])
                
            if _tasks["task_type"] == "nslookup":
                print("Start NSLOOKUP Task ID: " + _tasks["task_id"])
                ns_ip = _tasks["task_infos"]["ns_ip"]
                task_result = functions.nslookup(ns_ip)
                print("End NSLOOKUP Task ID: " + _tasks["task_id"])

            if task_result is not None:
                url = 'https://ipv64.net/dims/task_report_result.php'
                myobj = {'node_secret': node_secret, 'task_id': _tasks["task_id"], 'task_result': task_result}
                req = requests.post(url, data=myobj, verify=False)
    if x["verbose"] == 1:
        print(task_result)
    print("Wait for next Job.")
    time.sleep(x["wait"])

print(f"Response: {x.json()}")

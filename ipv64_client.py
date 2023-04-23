from pythonping import ping
import requests
import json
import time
import sys
import functions
import logging

node_id = "8g8893ff"
node_secret = sys.argv[1]

logging.info("IPv64.net - Initialisierung")

# At Start, report IPv4 and IPv6
functions.report_ipv4(node_secret)
functions.report_ipv6(node_secret)
functions.report_version(node_secret)

while(True):
    url = 'https://ipv64.net/dims/get_task.php'
    myobj = {'node_secret' : node_secret}

    x = requests.post(url, data = myobj)

    x = x.json()
    if x["report_ip"] == '1':
        functions.report_ipv4(node_secret)
        functions.report_ipv6(node_secret)
        logging.info("Report IPv4 & IPv6")
    if 'tasks' in x:
        for _tasks in x["tasks"]:
            task_result = None
            if(_tasks["task_type"] == "icmpv4"):
                logging.info(f"Start ICMPv4 Task ID: {_tasks['task_id']}")
                icmp_dst = _tasks["task_infos"]["icmp_dst"]
                icmp_size = _tasks["task_infos"]["icmp_size"]
                icmp_count = _tasks["task_infos"]["icmp_count"]
                icmp_interval = _tasks["task_infos"]["icmp_interval"]
                icmp_timeout = _tasks["task_infos"]["icmp_timeout"]

                task_result = functions.icmp(icmp_dst,icmp_size,icmp_count,icmp_interval,icmp_timeout)
                logging.debug(task_result)
                logging.info(f"End ICMPv4 Task ID: {_tasks['task_id']}")

            if(_tasks["task_type"] == "icmpv6"):
                logging.info("Start ICMPv6 Task ID: "+_tasks["task_id"])
                icmp_dst = _tasks["task_infos"]["icmp_dst"]
                icmp_size = _tasks["task_infos"]["icmp_size"]
                icmp_count = _tasks["task_infos"]["icmp_count"]
                icmp_interval = _tasks["task_infos"]["icmp_interval"]
                icmp_timeout = _tasks["task_infos"]["icmp_timeout"]

                task_result = functions.icmp(icmp_dst,icmp_size,icmp_count,icmp_interval,icmp_timeout)
                logging.debug(task_result)
                logging.info("End ICMPv6 Task ID: "+_tasks["task_id"])

            if(_tasks["task_type"] == "dns"):
                print("Start DNS Task ID: "+_tasks["task_id"])
                dns_query = _tasks["task_infos"]["dns_query"]
                dns_type = _tasks["task_infos"]["dns_type"]

                task_result = functions.dns_resolve(dns_query,dns_type)
                logging.debug(task_result)
                logging.info("End DNS Task ID: "+_tasks["task_id"])

            if task_result is not None:
                url = 'https://ipv64.net/dims/task_report_result.php'
                myobj = {'node_secret' : node_secret,'task_id':_tasks["task_id"],'task_result':task_result}
                req = requests.post(url, data = myobj)
    logging.info("Wait for next Job.")
    time.sleep(x["wait"])

logging.info(f"Response: {x.json()}")

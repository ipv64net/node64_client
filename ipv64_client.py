import requests, time, sys
import functions
import urllib3

#Hide verification message
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

node_secret = sys.argv[1]

print("IPv64.net - Initialisierung")
# At Start, report IPv4 and IPv6
functions.report_ipv4(node_secret)
functions.report_ipv6(node_secret)
functions.report_version(node_secret)

while True:
    url = 'https://ipv64.net/dims/get_task.php'
    myobj = {'node_secret': node_secret}

    x = requests.post(url, data=myobj, verify=False)

    x = x.json()
    if x["error"] == '1':
        print("Node Secret is wrong")
        break
    if x["report_ip"] == '1':
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
                print(task_result)
                print("End ICMPv4 Task ID: " + _tasks["task_id"])

            if _tasks["task_type"] == "icmpv6":
                print("Start ICMPv6 Task ID: " + _tasks["task_id"])
                icmp_dst = _tasks["task_infos"]["icmp_dst"]
                icmp_size = _tasks["task_infos"]["icmp_size"]
                icmp_count = _tasks["task_infos"]["icmp_count"]
                icmp_interval = _tasks["task_infos"]["icmp_interval"]
                icmp_timeout = _tasks["task_infos"]["icmp_timeout"]

                task_result = functions.icmp(icmp_dst, icmp_size, icmp_count, icmp_interval, icmp_timeout, 6)
                print(task_result)
                print("End ICMPv6 Task ID: " + _tasks["task_id"])

            if _tasks["task_type"] == "dns":
                print("Start DNS Task ID: " + _tasks["task_id"])
                dns_query = _tasks["task_infos"]["dns_query"]
                dns_type = _tasks["task_infos"]["dns_type"]

                task_result = functions.dns_resolve(dns_query, dns_type)
                print(task_result)
                print("End DNS Task ID: " + _tasks["task_id"])

            if task_result is not None:
                url = 'https://ipv64.net/dims/task_report_result.php'
                myobj = {'node_secret': node_secret, 'task_id': _tasks["task_id"], 'task_result': task_result}
                req = requests.post(url, data=myobj, verify=False)
    print("Wait for next Job.")
    time.sleep(x["wait"])

print(f"Response: {x.json()}")

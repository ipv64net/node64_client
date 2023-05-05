from icmplib import ping, traceroute
import requests
import json
import dns
from dns.resolver import Resolver
import signal
import sys

version = "0.0.4"

def report_version(node_secret, timeout = 1.5):
    url = 'https://ipv64.net/dims/report_node_status.php'
    myobj = {'node_secret' : node_secret,'version':version}
    try:
        x = requests.post(url, data = myobj, verify=False, timeout=timeout)
    except:
        print("")

def report_ipv4(node_secret, timeout = 1.5):
    url = 'https://ipv4.ipv64.net/dims/report_node_status.php'
    myobj = {'node_secret' : node_secret}
    try:
        x = requests.post(url, data = myobj, verify=False, timeout=timeout)
    except:
        print("Skip: IPv4 could not be resolved")

def report_ipv6(node_secret, timeout = 1.5):
    url = 'https://ipv6.ipv64.net/dims/report_node_status.php'
    myobj = {'node_secret' : node_secret}
    try:
        x = requests.post(url, data = myobj, verify=False, timeout=timeout)
    except:
        print("Skip: IPv6 could not be resolved")

def icmp(icmp_dst,icmp_size,icmp_count,icmp_interval,icmp_timeout,family):
    try:
        response_list = ping(icmp_dst, count=icmp_count, interval=icmp_interval, timeout=icmp_timeout, payload_size=icmp_size, family=family)
        rtt_avg = response_list.avg_rtt
        rtt_min = response_list.max_rtt
        rtt_max = response_list.min_rtt
        packet_loss = response_list.packet_loss
        jitter = response_list.jitter
        task_result = {"rtt_avg":rtt_avg,"rtt_min":rtt_min,"rtt_max":rtt_max,"packet_loss":packet_loss,"jitter":jitter,"error_msg":"0"}
    except:
        packet_loss = response_list.packet_loss
        task_result = {"error_msg":"timeout","packet_loss":packet_loss}
    data = json.dumps(task_result)
    return data

def trace(trace_dst,trace_size,trace_count,trace_interval,trace_timeout,max_hops,family):
    try:
        hops = traceroute(trace_dst,count=trace_count,interval=0.1,timeout=1,max_hops=30,family=family,payload_size=trace_size)
        last_distance = 0
        tracert = []
        dist = 0
        end_hops = 0

        for hop in hops:
            dist += 1
            if last_distance + 1 != hop.distance:
                task_result = {"distance":dist}
            else:
                task_result = {"distance":hop.distance,"address":hop.address,"rtt_avg":hop.avg_rtt,"packet_loss":hop.packet_loss,"jitter":hop.jitter,"is_alive":hop.is_alive,"error_msg":"0",}
            tracert.append(task_result)
            last_distance = hop.distance
        end_hops = {"hops":last_distance}
        tracert.append(end_hops)
    except:
        task_result = {"error_msg":"timeout","packet_loss":"1"}
    data = json.dumps(tracert)
    return data

def dns_resolve(query,query_type):
    result = Resolver()
    #result.nameservers = [nameserver]
    try:
        result = result.resolve(query,query_type)
        response_time = round(result.response.time * 100,4)
        records = []
        for IPval in result:
            records.append(IPval.to_text())
        data = {"rrset":records,"latency":response_time,"error":"no"}
    except:
        print("Could not be resolved")
        data = {"error":"Could not be resolved"}
    data = json.dumps(data)
    return data
    
def nslookup(query):
    try:
        data = []
        result = dns.resolver.resolve_address(query)
        for res in result:
            data = {"ptr":str(res),"error":"0"}
    except:
        print("Could not be resolved")
        data = {"error":"Could not be resolved"}
    data = json.dumps(data)
    return data

def signal_handler(sig, frame):
    if sig == signal.SIGINT:
        print('\nYou pressed Ctrl+C!\nExit Programm')
    if sig == signal.SIGTERM:
        print('\nExit Programm')
    sys.exit(0)


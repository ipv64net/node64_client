from icmplib import ping
import requests, json, time, dns, multiping
import dns.resolver

version = "0.0.1"

def report_version(node_secret):
    url = 'https://ipv64.net/dims/report_node_status.php'
    myobj = {'node_secret' : node_secret,'version':version}
    try:
        x = requests.post(url, data = myobj)
    except:
        print("")    

def report_ipv4(node_secret):
    url = 'https://ipv4.ipv64.net/dims/report_node_status.php'
    myobj = {'node_secret' : node_secret}
    try:
        x = requests.post(url, data = myobj)
    except:
        print("Skip: IPv4 could not be resolved")
    
def report_ipv6(node_secret):
    url = 'https://ipv6.ipv64.net/dims/report_node_status.php'
    myobj = {'node_secret' : node_secret}
    try:
        x = requests.post(url, data = myobj)
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
        
def dns_resolve(query,query_type):
    result = dns.resolver.Resolver()
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
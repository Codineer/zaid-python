
import subprocess
subprocess.call('pip install scapy',shell=True)
import scapy.all as scapy
# def get_arguments():
#     import optparse
#     parser = optparse.OptionParser()
#     parser.add_option("-i", '--ipaddress', dest="ip_ad", help="write your victim's ip")
#     options, arguments = parser.parse_args()
#     return options

def get_arguments():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", '--ipaddress', dest="ip_ad", help="write your victim's ip")
    options = parser.parse_args()
    return options

def scan(ip):
    arp_request = scapy.ARP(pdst=ip) #specified the ip or ips to which we want to sent a arp request
    broadcost = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")#used for getting an object ethernet frame which contains the destinmation mac and source mac
    arp_request_broadcast = broadcost/arp_request #combining the packets to make a single packet
    # print(arp_request_broadcast.psrc)
    # print(arp_request_broadcast.hwsrc)
    answered_list = scapy.srp(arp_request_broadcast , timeout=1,verbose=False)[0]#broadcast the packet and receives answered and unanswered packets.
    answered_list_1=[]
    for i in answered_list:#it contains more lists in the .each list in it consist of a broadcasted packet and a corresponding answered packet:
        dic1=dict()
        dic1['mac']=i[1].hwsrc
        dic1['ip']=i[1].psrc
        answered_list_1.append(dic1)
    return answered_list_1
    # print(answered_list.summary())#got the summary of all the answered ips in the subnet i.e we got there mac
    # print(unanswered.summary())
    # print(broadcost.summary())
    # arp_request.show()
    # broadcost.show()
    # print(arp_request_broadcast.summary())
    # arp_request_broadcast.show()#show() method gets more details of the packet

    # scapy.ls(scapy.Ether())
    # arp_request.pdst=ip
    # print(arp_request.summary())
    # scapy.ls(scapy.ARP()) used to list all the variables of the class specified

def print_scan(answerlist):
    print("IP\t\tMacaddress\n--------------------------------------------------------------------------")
    for i in answerlist:
        print(i['mac'],end="\t")
        print(i['ip'])

options=get_arguments()
print_scan(scan(options.ip_ad))


# See PyCharm help at https://www.jetbrains.com/help/pycharm/

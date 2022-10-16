import subprocess
import optparse
import re
def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option('-i', '--interface', dest="interface", help="change mac")
    parser.add_option('-m', '--mac', dest="newmac", help="new mac option")
    options, arguments = parser.parse_args()
    if not options.interface:
        parser.error("please specify the interface ")
    elif not options.newmac:
        parser.error("please specify the newmac ")
    return options

def change_mac(interface, new_mac):
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])
    print("mac address changing of "+interface)

def get_current_mac(interface):
    ifconfig_result = str(subprocess.check_output(["ifconfig", interface]))
    mac_address = re.search(r'\w\w:\w\w:\w\w:\w\w:\w\w:\w\w', ifconfig_result)
    if mac_address:
        return mac_address.group(0)
    else:
        print("could'nt find mac ")

options = get_arguments()

currentmac=get_current_mac(options.interface)
print("current mac "+str(currentmac))
change_mac(options.interface,options.newmac)
currentmac=get_current_mac(options.interface)
if currentmac==options.mac:
    print("mac changed")
else:
    print("sorry")
#subprocess.call("ifconfig "+interface+" down", shell=True)
#subprocess.call("ifconfig "+interface+" hw ether " +address, shell=True)
#subprocess.call("ifconfig "+interface+" up", shell=True)



# See PyCharm help at https://www.jetbrains.com/help/pycharm/

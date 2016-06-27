#!/usr/bin/python2

from scapy.all import *
from sys import argv

IFACE='eth0'

def myMAC(iface):
    fam,hw = get_if_raw_hwaddr(IFACE)
    hw = hw.encode("hex")
    return ':'.join(hw[i:i+2] for i in range(0, len(hw), 2))

def randomMAC():
    mac = [ 0xDE, 0xAD,
        random.randint(0x00, 0x29),
        random.randint(0x00, 0x7f),
        random.randint(0x00, 0xff),
        random.randint(0x00, 0xff) ]
    return ':'.join(map(lambda x: "%02x" % x, mac))

m = myMAC(IFACE)

myxid=random.randint(1, 900000000)

hostname="test" + m[-2:]
if (len(argv) == 2):
    hostname = argv[1]
    print("Using {} as a hostname".format(hostname))

opt114 = "abc"

dhcp_discover =  Ether(src=m,dst="ff:ff:ff:ff:ff:ff")/IP(src="0.0.0.0",dst="255.255.255.255")/UDP(sport=68,dport=67)/BOOTP(chaddr=[mac2str(m)],xid=myxid)/DHCP(options=[("message-type","discover"),("hostname",hostname),(114,opt114),"end"])

sendp(dhcp_discover,iface=IFACE)

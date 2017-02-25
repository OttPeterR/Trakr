from scapy.all import sniff
from config import ConfigHelper

def scan():
    interface = ConfigHelper.getWirelessCaptureInterface()

    sniff(iface=interface, prn=lambda x: x.show(), filter="tcp", store=0)
    print "Scanning..."
    return

def processPacket(p):
    print "got one"
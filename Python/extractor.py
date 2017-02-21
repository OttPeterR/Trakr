import pcapy
from scapy.all import *

def getMACs(pathToPcap):
    count = 0
    packets = rdpcap(pathToPcap)

    for packet in packets:
        count = count + 1
        print count
        print packet.addr1
        print




def test():
    getMACs("/Users/pott/Desktop/few.pcap")


if __name__ == '__main__':
    test()
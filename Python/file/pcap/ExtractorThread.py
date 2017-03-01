from scapy.all import *


import ThreadKeeper
import Packet


def extract(filePath):
    ThreadKeeper.incrementThreadCount()
    print "extracting from "+filePath

    packets = rdpcap(filePath)

    processedPackets = []

    for packet in packets:
        processedPackets += [Packet.makePacket(packet)]

    print len(processedPackets)

    ThreadKeeper.decrementThreadCount()
    return
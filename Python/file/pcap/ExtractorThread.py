from scapy.all import *


import ThreadKeeper
import PacketExtractor


def extract(filePath):
    ThreadKeeper.incrementThreadCount()
    print "extracting from "+filePath

    packets = rdpcap(filePath)

    processedPackets = []

    for packet in packets:
        processedPackets += [PacketExtractor.makePacket(packet)]

    print len(processedPackets)

    ThreadKeeper.decrementThreadCount()
    return
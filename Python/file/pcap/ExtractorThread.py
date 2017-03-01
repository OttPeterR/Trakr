from scapy.all import *


import ThreadKeeper
import Observation


def extract(filePath):
    ThreadKeeper.incrementThreadCount()
    print "extracting from "+filePath

    packets = rdpcap(filePath)

    observations = []

    for packet in packets:
        observations += [Observation.makeObservation(packet)]

    print len(observations)

    ThreadKeeper.decrementThreadCount()
    return
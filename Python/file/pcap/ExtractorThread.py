from scapy.all import *
from subprocess import call

import ThreadKeeper
import Observation


def extract(filePath):
    ThreadKeeper.incrementThreadCount()

    packets = rdpcap(filePath)
    __renamePcap(filePath)
    observations = []
    for packet in packets:
        observations += [Observation.makeObservation(packet)]


    dict = getUniqueMACs(observations)
    ThreadKeeper.decrementThreadCount()
    return




def getUniqueMACs(observations):
    ind = 0
    dict = {}
    address = ""

    for o in observations:
        # is this a new mac address?
        if o.mac not in dict:
            dict[o.mac] = ind
            ind = ind + 1

    print "unique: " + str(len(dict))
    return dict

def __renamePcap(filePath):
    if filePath.endswith("-unprocessed.pcap"):
        newFilePath = filePath[:-17]+".pcap"
        call(["mv", filePath, newFilePath])
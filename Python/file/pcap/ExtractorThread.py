from scapy.all import *


import ThreadKeeper
import Observation


def extract(filePath):
    ThreadKeeper.incrementThreadCount()

    packets = rdpcap(filePath)
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

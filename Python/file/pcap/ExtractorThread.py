from scapy.all import *
from subprocess import call

from database.relational import RollingDatabaseHelper
import ThreadKeeper
import Observation


def extract(filePath):
    ThreadKeeper.incrementThreadCount()

    packets = rdpcap(filePath)
    __renamePcap(filePath)
    observations = []
    for packet in packets:
        observations += [Observation.makeObservation(packet)]


    loadObservations(observations)

    dict = getUniqueMACs(observations)
    ThreadKeeper.decrementThreadCount()
    return


def loadObservations(observations):
    RollingDatabaseHelper.connect()
    for o in observations:
        RollingDatabaseHelper.loadPacket(o)

    RollingDatabaseHelper.commit()
    RollingDatabaseHelper.close()
    return




def getUniqueMACs(observations):
    ind = 0
    dict = {} #dictionary of unique MAC addresses
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
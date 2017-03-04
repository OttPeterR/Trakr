from scapy.all import *
from subprocess import call

from database.relational import RollingDatabaseHelper
from database.relational import BehaviorDatabaseHelper
from config.ConfigHelper import getKeepAllPcaps
import ThreadKeeper
import Observation


def extract(filePath, lat=0, long=0):
    ThreadKeeper.incrementThreadCount()

    packets = rdpcap(filePath)

    __handleOldPcapFile(filePath)

    observations = []
    for packet in packets:
        observations += [Observation.makeObservation(packet)]

    loadObservations(observations)
    getUniqueMACs(observations)

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
    newUnique = 0
    dict = {} #dictionary of unique MAC addresses
    address = ""

    BehaviorDatabaseHelper.connect()

    for o in observations:
        # is this a new mac address?
        if o.mac not in dict:
            dict[o.mac] = ind
            if BehaviorDatabaseHelper.addNewAddress(o.mac):
                newUnique = newUnique+1
            ind = ind + 1

    BehaviorDatabaseHelper.commit()
    BehaviorDatabaseHelper.close()

    print "new unique: " + str(newUnique)
    return






def __renamePcap(filePath):
    if filePath.endswith("-unprocessed.pcap"):
        newFilePath = filePath[:-17]+".pcap"
        call(["mv", filePath, newFilePath])

def __deletePcap(filePath):
    call(["rm", filePath])

def __handleOldPcapFile(filePath):
    if getKeepAllPcaps():
        __renamePcap(filePath)
    else:
        __deletePcap(filePath)
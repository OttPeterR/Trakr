from subprocess import call

from scapy.all import *

import Observation
from config.ConfigHelper import getKeepAllPcaps, getCaptureDuration
from database.relational import BehaviorDatabaseHelper
from database.relational import RollingDatabaseHelper
from management import ThreadKeeper

def extract(filePath, latitude=0, longitude=0, allowDeletion=True):

    ThreadKeeper.incrementThreadCount()

    packets = rdpcap(filePath)

    __handleOldPcapFile(filePath, allowDeletion)

    latitude, longitude = __fixLatLong(latitude, longitude)

    #rough estimate as how big the list might be
    #fill it, then see if more room needs to be made
    array_size = getCaptureDuration() * 400
    observations = [Observation]*array_size
    count = 0
    for packet in packets:
        if count < array_size:
            observations[count] = Observation.makeObservation(packet, latitude, longitude)
        else:
            observations += [Observation.makeObservation(packet, latitude, longitude)]
        count = count + 1

    #making sure to cut off any unused parts
    if count < array_size:
        observations = observations[:count]

    roll_conn = RollingDatabaseHelper.connect()
    beha_conn = BehaviorDatabaseHelper.connect()

    __loadObservations(roll_conn, observations)
    RollingDatabaseHelper.removeBadPackets(roll_conn)
    getUniqueMACs(beha_conn, observations)

    roll_conn.close()
    beha_conn.close()

    ThreadKeeper.decrementThreadCount()
    return

def __fixLatLong(latitude, longitude):
    try:
        latitude = int(latitude)
    except ValueError:
        latitude = 0

    try:
        longitude = int(longitude)
    except ValueError:
        longitude = 0
    return latitude, longitude


def __loadObservations(connection, observations):
    for o in observations:
        RollingDatabaseHelper.loadPacket(connection, o)
    connection.commit()
    return

def getUniqueMACs(connection, observations):
    ind = 0
    newUnique = 0
    dict = {} #dictionary of unique MAC addresses
    address = ""
    for o in observations:
        # is this a new mac address?
        if o.mac not in dict:
            dict[o.mac] = ind
            if BehaviorDatabaseHelper.addNewAddress(connection, o.mac, o.time):
                newUnique = newUnique+1
            ind = ind + 1

    print "new unique devices: " + str(newUnique)
    return



def __renamePcap(filePath):
    if filePath.endswith("-unprocessed.pcap"):
        newFilePath = filePath[:-17]+".pcap"
        call(["mv", filePath, newFilePath])

def __deletePcap(filePath):
    call(["rm", filePath])

def __handleOldPcapFile(filePath, allowDeletion):
    if getKeepAllPcaps():
        __renamePcap(filePath)
    else:
        if allowDeletion:
            __deletePcap(filePath)
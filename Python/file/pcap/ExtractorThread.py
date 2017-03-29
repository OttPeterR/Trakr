from subprocess import call

import Observation
from config.ConfigHelper import getKeepAllPcaps, getCaptureDuration, getCaptureDirectory
from database.relational import BehaviorDatabaseHelper
from database.relational import RollingDatabaseHelper
from management import ThreadKeeper


def extract(filePath, latitude=0, longitude=0, allowDeletion=True):
    ThreadKeeper.incrementThreadCount()

    command = ["tshark", "-nr", filePath, "-N", "m",  # select the file for reading
               "-T", "fields",  # specify some fields to print out:
               "-e", "wlan.sa_resolved",  # print out the MAC
               "-e", "frame.time_epoch",  # print out the epoch time
               "-E", "separator=,"]  # separate the values with a comma
    try:
        # running process with output redirected to file
        #TODO make this file exist only in memory
        outputFilePath = __makeNewOutputFile()
        with open(outputFilePath, 'w') as out:
            call(command, stdout=out)

        # cleaning up temp file
        call(["rm", outputFilePath])

    except Exception, errmsg:
        print "Extraction failed."
        try:
            print "\tPerhaps tshark cannot be found\n\ttshark location:"
            call(["which", "tshark"])
        except Exception, innererr:
            pass
        print errmsg

    return False

    __handleOldPcapFile(filePath, allowDeletion)

    latitude, longitude = __fixLatLong(latitude, longitude)

    # rough estimate as how big the list might be
    # fill it, then see if more room needs to be made
    array_size = getCaptureDuration() * 400
    observations = [Observation] * array_size
    count = 0
    packets = []
    for packet in packets:
        if count < array_size:
            observations[count] = Observation.makeObservation(packet, latitude, longitude)
        else:
            observations += [Observation.makeObservation(packet, latitude, longitude)]
        count = count + 1

    # done with packets, remove from memory
    del packets

    # making sure to cut off any unused parts
    if count < array_size:
        observations = observations[:count]

    conn_rolling = RollingDatabaseHelper.connect()
    conn_behavior = BehaviorDatabaseHelper.connect()

    __loadObservations(conn_rolling, observations)
    RollingDatabaseHelper.removeBadPackets(conn_rolling)
    getUniqueMACs(conn_behavior, observations)

    # done with observations, remove it from memory
    del observations

    conn_rolling.close()
    conn_behavior.close()

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
    dict = {}  # dictionary of unique MAC addresses
    address = ""
    for o in observations:
        # is this a new mac address?
        if o.mac not in dict:
            dict[o.mac] = ind
            if BehaviorDatabaseHelper.addNewAddress(connection, o.mac, o.time):
                newUnique = newUnique + 1
            ind = ind + 1

    print "new unique devices: " + str(newUnique)
    return


def __renamePcap(filePath):
    if filePath.endswith("-unprocessed.pcap"):
        newFilePath = filePath[:-17] + ".pcap"
        call(["mv", filePath, newFilePath])


def __deletePcap(filePath):
    call(["rm", filePath])


def __handleOldPcapFile(filePath, allowDeletion):
    if getKeepAllPcaps():
        __renamePcap(filePath)
    else:
        if allowDeletion:
            __deletePcap(filePath)


def __makeNewOutputFile():
    path = getCaptureDirectory() + "temp_" + ThreadKeeper.getTimeStamp() + ".txt"
    return path

import Observation
from subprocess import call
from management import ThreadKeeper
from config.ConfigHelper import getCaptureDirectory, getCaptureDuration, getKeepAllPcaps


def extractToObservations(filePath, latitude, longitude, allowDeletion):
    array_size = getCaptureDuration() * 400
    observations = [Observation] * array_size
    packets = []

    outFile = None
    try:
        # running process with output redirected to file
        # TODO make this file exist only in memory
        outputFilePath = __makeNewOutputFile()
        outFile = open(outputFilePath, 'w')
    except Exception, errmsg:
        print "Error with creating temp file:"
        print errmsg
        return False
        print outFile.name
    try:
        command = ["tshark", "-nr", filePath, "-N", "m",  # select the file for reading
                   "-T", "fields",  # specify some fields to print out:
                   "-e", "wlan.ta_resolved",  # print out the MAC
                   "-e", "frame.time_epoch",  # print out the epoch time
                   "-E", "separator=,"]  # separate the values with a comma
        call(command, stdout=outFile)
        # TODO fill 'packets' array with stuff when you read the file, tuple of (address, time)
        for line in outFile:
            packets += ("addr", 12345)
            # regex the line, it will be one of the two (with no spaces)
            # address,time
            # ,time
            # if its just a time, skip it
            pass
    except Exception, errmsg:
        print "Error while calling tshark for extraction:"
        print errmsg

        # cleaning up temp file
        call(["rm", outputFilePath])

    # deleting the old pcap that was just read in
    __handleOldPcapFile(filePath, allowDeletion)

    # making these into ints just to be sure
    latitude, longitude = __fixLatLong(latitude, longitude)

    count = 0
    for packet in packets:
        # packet is a tuple of (address, time)
        if count < array_size:
            observations[count] = Observation.makeObservation(packet[1], packet[0], latitude, longitude)
        else:
            observations += [Observation.makeObservation(packet[1], packet[0], latitude, longitude)]
        count = count + 1

    # done with packets, remove from memory
    del packets

    # making sure to cut off any unused parts
    if count < array_size:
        observations = observations[:count]


def __makeNewOutputFile():
    path = getCaptureDirectory() + "temp_" + ThreadKeeper.getTimeStamp() + ".txt"
    return path


def __handleOldPcapFile(filePath, allowDeletion):
    if getKeepAllPcaps():
        __renamePcap(filePath)
    else:
        if allowDeletion:
            __deletePcap(filePath)


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


def __renamePcap(filePath):
    if filePath.endswith("-unprocessed.pcap"):
        newFilePath = filePath[:-17] + ".pcap"
        call(["mv", filePath, newFilePath])


def __deletePcap(filePath):
    call(["rm", filePath])

import Observation
from subprocess import call
from management import ThreadKeeper
from config.ConfigHelper import getCaptureDirectory, getCaptureDuration, getKeepAllPcaps


def extractToObservations(filePath, latitude, longitude, allowDeletion):
    # make a file path that will be used
    outputFilePath = __makeNewOutputFile()
    # if successfully extracted data
    if __extractToFile(filePath, outputFilePath):
        # then turn it into observations and return it
        return __processTempFile(filePath, latitude, longitude, allowDeletion, outputFilePath)
    # otherwise just return an empty list
    else:
        return []


def __extractToFile(filePath, outputFilePath):
    try:
        # running process with output redirected to file
        # TODO make this file exist only in memory
        outFile = open(outputFilePath, 'w')

        ##### start tshark command section
        try:
            command = ["tshark", "-nr", filePath, "-N", "m",  # select the file for reading
                       "-T", "fields",  # specify some fields to print out:
                       "-e", "wlan.ta_resolved",  # print out the MAC
                       "-e", "frame.time_epoch",  # print out the epoch time
                       "-E", "separator=,"]  # separate the values with a comma

            call(command, stdout=outFile)
            outFile.close()

        except Exception, errmsg:
            print "Error while calling tshark for extraction:"
            print errmsg

            ##### end tshark command section

    except Exception, errmsg:
        print "Error with creating temp file:"
        print errmsg
        return False
    return True


def __processTempFile(filePath, latitude, longitude, allowDeletion, outputFilePath):
    packets = []
    tempFile = open(outputFilePath, 'r')
    # now process the file
    for line in tempFile:
        # TODO fill 'packets' array with stuff when you read the file, tuple of (time, address)
        # regex the line, it will be one of the two (with no spaces)
        # address,time
        # ,time
        # if its just a time, skip it
        pass

    # cleaning up temp file
    call(["rm", outputFilePath])

    # deleting the old pcap that was just read in
    __handleOldPcapFile(filePath, allowDeletion)

    # making these into ints just to be sure
    latitude, longitude = __fixLatLong(latitude, longitude)
    observations = []
    for packet in packets:
        # packet is a tuple of (time, address)
        observations += [Observation.makeObservation(packet[0], packet[1], latitude, longitude)]
    return observations


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

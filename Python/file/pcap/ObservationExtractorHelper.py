import Observation
from subprocess import call
from management import ThreadKeeper
from config.ConfigHelper import getCaptureDirectory, getCaptureDuration, getKeepAllPcaps

separator = '$'


def extractToObservations(filePath, latitude, longitude, allowDeletion):
    # make a file path that will be used
    print "Reading: " + filePath + "\r"
    outputFilePath = __makeNewOutputFile()

    extracted = __extractToFile(filePath, outputFilePath)
    # if successfully extracted data
    if extracted:
        # then turn it into observations and return it
        return __processTempFile(filePath, latitude, longitude, allowDeletion, outputFilePath)
    # otherwise just return an empty list
    else:
        return []


def __extractToFile(filePath, outputFilePath):
    outFile = None

    try:
        # running process with output redirected to file
        # TODO make this file exist only in memory
        outFile = open(outputFilePath, 'w')

        ##### start tshark command section
        try:
            command = ["tshark", "-nr", filePath, "-N", "m",  # select the file for reading
                       "-T", "fields",  # specify some fields to print out:
                       "-e", "wlan.ta_resolved",  # print out the MAC (transmission address)
                       "-e", "frame.time_epoch",  # print out the epoch time
                       "-E", "separator=" + separator]  # separate the values

            call(command, stdout=outFile)

        except Exception, errmsg:
            print "Error while calling tshark for extraction:"
            print errmsg
            ##### end tshark command section

    except Exception, errmsg:
        print "Error with creating temp file:"
        print errmsg
        return False
    return outFile


def __processTempFile(filePath, latitude, longitude, allowDeletion, outputFilePath):
    # open the tempFile of values
    tempFile = open(outputFilePath, 'r')

    # fill the array with line reads
    packets = []
    count = 0
    for line in tempFile:
        # if the line has info that's useful
        if len(line) > 0:
            if (line[0] != ','):
                # make a tuple out of it (time, address)
                addr, time = line.split(separator)
                packets += [(time, addr)]
                count = count + 1
                print '{0}\r'.format("  values: " + str(count)),
    print

    # cleaning up temp file
    tempFile.close()
    call(["rm", outputFilePath])

    # deleting the old pcap that was just read in
    __handleOldPcapFile(filePath, allowDeletion)

    # making these into ints just to be sure
    latitude, longitude = __fixLatLong(latitude, longitude)

    observations = [Observation] * count
    total = count
    count = 0
    for packet in packets:
        # packet is a tuple of (time, address)
        observations[count] = Observation(packet[0], packet[1], latitude, longitude)
        count = count + 1
        print '{0}\r'.format("  processing: " + str(100 * count / total) + "%\n"),
    print
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

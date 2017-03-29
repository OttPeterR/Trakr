from subprocess import call

from config import ConfigHelper
from file.pcap import Extractor
from management import ThreadKeeper


def scanLoop(loadToDabatase, lat=0, long=0):
    while True:
        pcapPath = scan()
        if loadToDabatase:
            Extractor.ExtractFromFile(pcapPath, lat, long)


def scan():
    ThreadKeeper.incrementThreadCount()

    captureInterface = str(ConfigHelper.getWirelessCaptureInterface())
    captureDuration = str(ConfigHelper.getCaptureDuration())

    capturePath = str(ConfigHelper.getCaptureDirectory()) + \
                  ThreadKeeper.getTimeStamp() + \
                  "-unprocessed.pcap"

    try:
        # making the saved pcap able to be deleted by normal users since it was created with root
        call(["touch", capturePath])
        call(["chmod", "777", capturePath])
    except Exception, errmsg:
        print "Could not change output file permissions, you might need root permissions to delete it now, sorry about that..."
        print errmsg

    try:
        output = open("/dev/null", "wr")

        # tshark -I -i CAPTURE_INTERFACE -a duration:CAPTURE_DURATION -w OUTPUT_FILE.pcap
        command = ["tshark",
                   "-I",  # monitor mode
                   "-i", captureInterface,  # capture interface
                   "-a", ("duration:" + captureDuration),  # run time
                   "-w", capturePath]  # where to save the file
        call(command, stdout=None)  # redirecting the output to null

    except Exception, errmsg:
        print "Scan thread failed while running:"
        print errmsg

    ThreadKeeper.decrementThreadCount()
    return capturePath

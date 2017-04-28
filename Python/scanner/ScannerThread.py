from subprocess import call, Popen
from os import devnull, waitpid

from config import ConfigHelper
from file.pcap import Extractor
from management import ThreadKeeper
from analysis import BehaviorReducer

def scanLoop(loadToDabatase, lat=0, long=0, analyze=False):
    print "Scanning..."
    while True:
        pcapPath = scan()
        if loadToDabatase:
            Extractor.extractFromFile(pcapPath, lat, long)
        if analyze:
            BehaviorReducer.beginAnalysis()


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
        # tshark -I -i CAPTURE_INTERFACE -a duration:CAPTURE_DURATION -w OUTPUT_FILE.pcap
        command = ["tshark",
                   "-I",  # monitor mode
                   "-i", captureInterface,  # capture interface
                   "-a", ("duration:" + captureDuration),  # run time
                   "-w", capturePath]  # where to save the file
        #with open(devnull, 'wb') as outNull:
        #    call(command, stdout=outNull)  # redirecting the output to null, doesn't work though
        p = Popen(" ".join(command)+" > /dev/null 2>&1", shell=True)
        waitpid(p.pid, 0)

    except Exception, errmsg:
        print "Scan thread failed while running:"
        print errmsg

    ThreadKeeper.decrementThreadCount()
    return capturePath

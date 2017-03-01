#from scapy.all import sniff
from config import ConfigHelper
from subprocess import call
from file import Extractor
import ThreadKeeper



def scanLoop():
    while True:
        pcapPath = scan()
        Extractor.ExtractFromFile(pcapPath)


def scan():

    ThreadKeeper.incrementThreadCount()

    captureInterface = str(ConfigHelper.getWirelessCaptureInterface())
    captureDuration = str(ConfigHelper.getCaptureDuration())

    captureDirectory = str(ConfigHelper.getTRAKrFullPath())
    capturePath = captureDirectory + "/scanner/output/" + \
                  ThreadKeeper.getTimeStamp() + \
                  "-unprocessed.pcap"

    try:
        # making the saved pcap able to be deleted by normal users since it was created with root
        call(["touch", capturePath])
        call(["chmod", "777", capturePath])
    except Exception, errmsg:
        print "Could not change output file permissions, you'll need root permissions to delete it now, sorry about that..."
        print errmsg

    try:
        print "New thread is scanning..."
        # tshark -I -i CAPTURE_INTERFACE -a duration:CAPTURE_DURATION -w OUTPUT_FILE.pcap
        call(["tshark",
                         "-I",  #monitor mode
                         "-i", captureInterface, # capture interface
                         "-a", ("duration:"+captureDuration), # run time
                         "-w", capturePath])

    except Exception, errmsg:
        print "Scan thread failed while running:"
        print errmsg

    ThreadKeeper.decrementThreadCount()
    return capturePath
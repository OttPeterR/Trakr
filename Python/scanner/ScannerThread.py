#from scapy.all import sniff
from config import ConfigHelper
from subprocess import call
import ThreadKeeper

def scan():
    ThreadKeeper.incrementThreadCount()
    try:
        print "New thread is scanning..."

        captureInterface = str(ConfigHelper.getWirelessCaptureInterface())
        captureDuration = str(ConfigHelper.getCaptureDuration())

        captureDirectory = str(ConfigHelper.getTRAKrFullPath())
        capturePath = captureDirectory + "/scanner/output/" + \
                      ThreadKeeper.getTimeStamp() + \
                      "-unprocessed.pcap"

        # tshark -I -i CAPTURE_INTERFACE -a duration:CAPTURE_DURATION -w OUTPUT_FILE.pcap
        call(["tshark",
                         "-I",  #monitor mode
                         "-i", captureInterface, # capture interface
                         "-a", ("duration:"+captureDuration), # run time
                         "-w", capturePath])

        # making the saved pcap able to be deleted by normal users since it was created with root
        call(["chmod", "777", capturePath])


    except Exception, errmsg:
        print "Scan thread failed while running:"
        print errmsg
    ThreadKeeper.decrementThreadCount()
    return

def processPacket(p):
    print "got one"

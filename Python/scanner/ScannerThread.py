#from scapy.all import sniff
from config import ConfigHelper
from subprocess import call
import ThreadKeeper

def scan():
    ThreadKeeper.incrementThreadCount()

    print "New thread is scanning..."
    captureDirectory = str(ConfigHelper.getTRAKrFullPath())
    captureInterface = str(ConfigHelper.getWirelessCaptureInterface())
    captureDuration = str(ConfigHelper.getCaptureDuration())

    # tshark-I -i CAPTURE_INTERFACE -a duration:CAPTURE_DURATION -w OUTPUT_FILE.pcap
    call(["tshark",
                     "-I",  #monitor mode
                     "-i", captureInterface, # capture interface
                     "-a", ("duration:"+captureDuration), # run time
                     "-w", "capture.pcap"])

    ThreadKeeper.decrementThreadCount()
    return


def processPacket(p):
    print "got one"

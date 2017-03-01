from scapy.all import *

import ThreadKeeper

def extract(filePath):
    ThreadKeeper.incrementThreadCount()
    print "extracting from "+filePath

    packets = rdpcap(filePath)


    ThreadKeeper.decrementThreadCount()
    return
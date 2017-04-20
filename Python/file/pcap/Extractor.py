import thread

import ExtractorThread
import os


def start(filePath, lat, long, allowDeletion):
    ExtractorThread.extract(filePath, lat, long, allowDeletion)

def extractFromFile(filePath, lat, long, allowDeletion=True):
    try:
        thread.start_new_thread(start, (filePath, lat, long, allowDeletion))
    except Exception, errmsg:
        print "Extraction thread failed to start:"
        print errmsg



def extractFromDir(path, lat, long, allowDeletion=True):
    try:
        for f in os.listdir(path):
            if f.endswith(".pcap"):
                start(path+f, lat, long, allowDeletion)
    except Exception, errmsg:
        print "Extraction thread failed to start:"
        print errmsg
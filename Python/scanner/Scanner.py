import thread
from scanner import ScannerThread
import ThreadKeeper

def startScan():
    ScannerThread.scan()


def beginScan():
    numThreads = ThreadKeeper.getNumThreads()
    try:
        thread.start_new_thread(startScan, ())
    except Exception, errmsg:
        print "Scan thread failed to start:"
        print errmsg
import thread

from management import ThreadKeeper
from scanner import ScannerThread


def start(loadToDabatase, analyze):

    ThreadKeeper.incrementThreadCount()
    lat =  0#raw_input("  Please input Latitude:  ")
    long = 0#raw_input("  Please input Longitude: ")
    ScannerThread.scanLoop(loadToDabatase, lat, long, analyze)
    ThreadKeeper.decrementThreadCount()

def beginScan(loadToDabatase, analyze):
    try:
        thread.start_new_thread(start, (loadToDabatase, analyze))
    except Exception, errmsg:
        print "Scan thread failed to start:"
        print errmsg
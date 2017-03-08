import thread

from management import ThreadKeeper
from scanner import ScannerThread


def start(loadToDabatase):

    ThreadKeeper.incrementThreadCount()
    lat = raw_input("  Please input Latitude:")
    long = raw_input("  Please input Longitude:")
    ScannerThread.scanLoop(loadToDabatase, lat, long)
    ThreadKeeper.decrementThreadCount()

def beginScan(loadToDabatase):
    try:
        thread.start_new_thread(start, (loadToDabatase,))
    except Exception, errmsg:
        print "Scan thread failed to start:"
        print errmsg
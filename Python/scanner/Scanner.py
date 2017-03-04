import thread
from scanner import ScannerThread
import ThreadKeeper

def start(alsoAnalyze):

    ThreadKeeper.incrementThreadCount()
    lat = raw_input("  Please input Latitude:")
    long = raw_input("  Please input Longitude:")
    ScannerThread.scanLoop(alsoAnalyze, lat, long)
    ThreadKeeper.decrementThreadCount()

def beginScan(alsoAnalyze):
    try:
        thread.start_new_thread(start, (alsoAnalyze,))
    except Exception, errmsg:
        print "Scan thread failed to start:"
        print errmsg
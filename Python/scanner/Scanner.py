import thread
from scanner import ScannerThread

def start(alsoAnalyze):

    lat = raw_input("Please input Latitude:")
    #lat = 0

    long = raw_input("Please input Longitude:")
    #long = 0
    ScannerThread.scanLoop(alsoAnalyze, lat, long)


def beginScan(alsoAnalyze):
    try:
        thread.start_new_thread(start, (alsoAnalyze,))
    except Exception, errmsg:
        print "Scan thread failed to start:"
        print errmsg
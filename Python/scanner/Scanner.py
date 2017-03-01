import thread
from scanner import ScannerThread

def start(alsoAnalyze):
    ScannerThread.scanLoop(alsoAnalyze)


def beginScan(alsoAnalyze):
    try:
        thread.start_new_thread(start, (alsoAnalyze,))
    except Exception, errmsg:
        print "Scan thread failed to start:"
        print errmsg
import thread
from scanner import ScannerThread

def startScan():
    ScannerThread.scanLoop()


def beginScan():
    try:
        thread.start_new_thread(startScan, ())
    except Exception, errmsg:
        print "Scan thread failed to start:"
        print errmsg
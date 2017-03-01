import thread
from scanner import ScannerThread

def start():
    ScannerThread.scanLoop()


def beginScan():
    try:
        thread.start_new_thread(start, ())
    except Exception, errmsg:
        print "Scan thread failed to start:"
        print errmsg
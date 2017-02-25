import thread
from scanner import ScannerThread


def beginScan():
    print "Starting WiFi Capture Thread..."
    thread.start_new(ScannerThread.scan())


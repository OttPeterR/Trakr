import thread
from scanner import ScannerThread


def beginScan():
    thread.start_new(ScannerThread.scan())


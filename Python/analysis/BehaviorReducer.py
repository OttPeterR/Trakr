import thread
from analysis import BehaviorReducerThread

def analyze(dbPath):
    BehaviorReducerThread.analyze(dbPath)


def beginAnalysis(dbPath):
    try:
        thread.start_new_thread(analyze, (dbPath))
    except Exception, errmsg:
        print "Pcap analysis failed to start:"
        print errmsg
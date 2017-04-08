import thread
from analysis import BehaviorReducerThread
from management import ThreadKeeper

def __analyze():
    ThreadKeeper.incrementThreadCount()
    BehaviorReducerThread.analyze()
    ThreadKeeper.decrementThreadCount()

def beginAnalysis():
    try:
        thread.start_new_thread(__analyze, ())
    except Exception, errmsg:
        print "Pcap analysis failed to start:"
        print errmsg
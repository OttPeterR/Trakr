import thread
from management import ThreadKeeper
import ReducedDataProcessorThread

def __export():
    ThreadKeeper.incrementThreadCount()
    ReducedDataProcessorThread.makeExportData()
    ThreadKeeper.decrementThreadCount()

def beginExport():
    try:
        thread.start_new_thread(__export, ())
    except Exception, errmsg:
        print "Export failed to start:"
        print errmsg
import thread
from management import ThreadKeeper
import ReducedDataProcessorThread
from file.export import CSVWriter

def __export(filepath):
    ThreadKeeper.incrementThreadCount()
    data = ReducedDataProcessorThread.makeExportData()
    CSVWriter.export(filepath, data)
    ThreadKeeper.decrementThreadCount()

def beginExport(filepath):
    try:
        thread.start_new_thread(__export, (filepath,))
    except Exception, errmsg:
        print "Export failed to start:"
        print errmsg
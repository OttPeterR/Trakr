import thread
import ExtractorThread

def start(filePath):
    ExtractorThread.extract(filePath)

def ExtractFromFile(filePath):
    try:
        thread.start_new_thread(start, (filePath,))
    except Exception, errmsg:
        print "Extraction thread failed to start:"
        print errmsg
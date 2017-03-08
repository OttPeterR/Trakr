import thread

import ExtractorThread


def start(filePath, lat, long, allowDeletion):
    ExtractorThread.extract(filePath, lat, long, allowDeletion)

def ExtractFromFile(filePath, lat, long, allowDeletion=True):
    try:
        thread.start_new_thread(start, (filePath, lat, long, allowDeletion))
    except Exception, errmsg:
        print "Extraction thread failed to start:"
        print errmsg
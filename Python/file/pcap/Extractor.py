import thread

import ExtractorThread


def start(filePath, lat, long):
    ExtractorThread.extract(filePath, lat, long)

def ExtractFromFile(filePath, lat, long):
    try:
        thread.start_new_thread(start, (filePath, lat, long))
    except Exception, errmsg:
        print "Extraction thread failed to start:"
        print errmsg
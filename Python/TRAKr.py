import os

import cli.app

from config import ConfigHelper
from database import DatabaseExporter
from file.pcap import Extractor
from database import DatabaseInit
from management import ThreadKeeper
from scanner import Scanner


@cli.app.CommandLineApp
def TRAKr(app):

    ThreadKeeper.incrementThreadCount()

    configHelper = ConfigHelper.ConfigHelper()
    configHelper.startUp()

    # handling pre-run parameters first
    if TRAKr.params.reset:
        configHelper.resetConfig()

    if TRAKr.params.export:
        DatabaseExporter.exportDatabases()

    elif TRAKr.params.delete_databases:
        __deleteDBs()
        __initDBs()



    # handling run parameters

    if TRAKr.params.run:
        __run()
    else:
        if TRAKr.params.scan:
            __scan(True)

        #if TRAKr.params.loadfile:
        #    __loadFile(path, lat, long)


        if TRAKr.params.analyze:
            __analyze()

    ThreadKeeper.decrementThreadCount()
    ThreadKeeper.wait(0.01)
    ThreadKeeper.waitForThreads()
    #print("[TRAKr] - Shutting Down")



# Helper functions to do the things

def __scan(loadToDabatase):
    # root check
    if os.geteuid() == 0:
        # we're good to go, let's scan, this will loop infinitely
        __initDBs()
        Scanner.beginScan(loadToDabatase)
    else:
        # sucks. no scanning today
        print "Please run as root to capture packets."
        os._exit(0)
    return

def __analyze():
    __initDBs()
    # call analysis to process the folder of stuff
    return

def __run():
    __initDBs()
    __scan(True) #while running a single instance, scan will call it's own analysis
    return



def __loadFile(path, latitude, longitude):
    Extractor.ExtractFromFile(path, latitude, longitude)

def __initDBs():
    DatabaseInit.initDBs()

def __deleteDBs():
    DatabaseInit.deleteDBs()

def __removePcaps():
    # http://stackoverflow.com/questions/1995373/
    path = str(ConfigHelper.getCaptureDirectory())
    [os.remove(path+f) for f in os.listdir(path) if f.endswith(".pcap")]


# for operational things, use a parameter that gets set
TRAKr.add_param("-r", "--run", help="this starts capture and analysis processing all-in-one. Needs root permissions",
                action='store_true')
TRAKr.add_param("-s", "--scan", help="begin scanning and saving to the database", action='store_true')
#TRAKr.add_param("-l","--loadfile",help="loads a pcap file into the database", action='store_true')
TRAKr.add_param("-reset", "--reset", help="resets the config file to defaul", action='store_true')
TRAKr.add_param("-exp", "--export", help="export the rolling.db, reduced.db, and graph.db into the /export dir",
                action='store_true', default=False)
TRAKr.add_param("-delDB", "--delete_databases", help="delete all databases and create new ones.", action='store_true', default=False)
TRAKr.add_param("-a", "--analyze", help="run analysis on packets", action='store_true')

#TODO params to add:
#   -i import pcap from file or directory for analysis, remember to ask for lat/long



if __name__ == '__main__':
    try:
        TRAKr.run()
        #catch the keyboard interrupt and cleanup half open files
    except KeyboardInterrupt:
        print "\nTRAKr - Shutting down...\n"
        __removePcaps()
        os._exit(0)

import cli.app
import os
import SystemEvents

import ThreadKeeper
from scanner import Scanner
from config import ConfigHelper
from database import DatabaseExporter
from database import DatabaseInit


@cli.app.CommandLineApp
def TRAKr(app):


    #print "[TRAKr] - Starting Up"
    # make sure the settings are all loaded up and good

    configHelper = ConfigHelper.ConfigHelper()
    configHelper.startUp()

    needToWait = False

    # handling pre-run parameters first
    if TRAKr.params.reset:
        configHelper.resetConfig()

    if TRAKr.params.export_databases:
        needToWait = True
        DatabaseExporter.exportDatabases()

    elif TRAKr.params.delete_databases:
        __deleteDBs()
        __initDBs()



    # handling run parameters

    if TRAKr.params.run:
        __run()
    else:
        if TRAKr.params.scan:
            needToWait = True
            __scan(True)

        if TRAKr.params.analyze:
            __analyze()



    #done with all the parameters, now we just finish up

    if needToWait:
        # giving the params a chance to start their threads
        ThreadKeeper.wait(3)

    ThreadKeeper.waitForThreads()
    #print("[TRAKr] - Shutting Down")



# Helper functions to do the things

def __scan(alsoAnalyze):
    # root check
    if os.geteuid() == 0:
        # we're good to go, let's scan, this will loop infinitely
        __initDBs()
        Scanner.beginScan(alsoAnalyze)
    else:
        # sucks. no scanning today
        print "Please run as root to capture packets. Exiting..."
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
TRAKr.add_param("-reset", "--reset", help="resets the config file to defaul", action='store_true')
TRAKr.add_param("-db", "--export_databases", help="export the rolling.db, reduced.db, and graph.db into the /export dir",
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

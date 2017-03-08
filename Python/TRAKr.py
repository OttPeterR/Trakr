import os

import cli.app

from config import ConfigHelper
from database import DatabaseExporter
from file.pcap import Extractor
from database import DatabaseInit
from management import ThreadKeeper
from scanner import Scanner


# this is what runs when the command line application is invoked
@cli.app.CommandLineApp
def TRAKr(app):
    # loading up the config file parser
    configHelper = ConfigHelper.ConfigHelper()
    configHelper.startUp()

    # handling pre-run parameters first
    if TRAKr.params.reset:
        configHelper.resetConfig()

    # exporting databases
    if TRAKr.params.export:
        DatabaseExporter.exportDatabases()

    # deleting databases
    elif TRAKr.params.delete_databases:
        __deleteDBs()
        __initDBs()

    # handling run-oriented parameters
    # these are the ones that can go infinitely like scans
    if TRAKr.params.run:
        __run()
    else:
        # this only scans and puts the MACs into the rolling.db
        if TRAKr.params.scan:
            __scan(True)

        # load up a file, lat/long will be 0 as default if not inputted
        if TRAKr.params.loadfile != "":
            __loadFile(TRAKr.params.loadfile, TRAKr.params.latitude, TRAKr.params.longitude)

        # run analysis on rolling.db
        if TRAKr.params.analyze:
            __analyze()

    # wait just a little bit, because sometimes it'll race condition and go past this
    ThreadKeeper.wait(0.01)

    # don't stop execution just yet, because scan or analysis may be running
    ThreadKeeper.waitForThreads()
    # print("[TRAKr] - Shutting Down")


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
    # call analysis to process the folder of databases
    # also look for a subfolder called importme - that will contain other
    #   rolling.db that need to be consolidated into one big one
    return


# all-in-one solution for doing everything
def __run():
    __initDBs()
    __scan(True)  # while running a single instance, scan will call it's own analysis
    __analyze()
    return


# loads a pcap file into the rolling.db
def __loadFile(path, latitude, longitude):
    print "Loading " + str(path) + " at: (" + str(latitude) + ", " + str(longitude) + ")"
    Extractor.ExtractFromFile(path, latitude, longitude, False)


# it's okay to call this multiple times, it just makes sure that everything is there
def __initDBs():
    DatabaseInit.initDBs()


# removes database files, does not recreate them
def __deleteDBs():
    DatabaseInit.deleteDBs()


# deletes all pcap files in the folder, this is a little dangerous
def __removePcaps():
    # http://stackoverflow.com/questions/1995373/
    path = str(ConfigHelper.getCaptureDirectory())
    [os.remove(path + f) for f in os.listdir(path) if f.endswith(".pcap")]


# for operational things, use a parameter that gets set
TRAKr.add_param("-r", "--run", help="this starts capture and analysis processing all-in-one. Needs root permissions",
                action='store_true')
TRAKr.add_param("-s", "--scan", help="begin scanning and saving to the database", action='store_true')
TRAKr.add_param("-reset", "--reset", help="resets the config file to defaul", action='store_true')
TRAKr.add_param("-exp", "--export", help="export the rolling.db, reduced.db, and graph.db into the /export dir",
                action='store_true', default=False)
TRAKr.add_param("-delDB", "--delete_databases", help="delete all databases and create new ones.", action='store_true',
                default=False)
TRAKr.add_param("-a", "--analyze", help="run analysis on packets", action='store_true')

TRAKr.add_param("-l", "--loadfile", type=str, default="", help="loads a pcap file into the database")
TRAKr.add_param("-lat", "--latitude", type=float, default=0)
TRAKr.add_param("-long", "--longitude", type=float, default=0)

# TODO params to add:
#   -i import pcap from file or directory for analysis, remember to ask for lat/long



if __name__ == '__main__':
    try:
        TRAKr.run()
        # catch the keyboard interrupt and cleanup half open files
    except KeyboardInterrupt:
        print "\nTRAKr - Shutting down...\n"
        __removePcaps()
        os._exit(0)

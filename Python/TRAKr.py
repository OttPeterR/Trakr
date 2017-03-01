import cli.app
import os

import ThreadKeeper

from scanner import Scanner
from config import ConfigHelper
from database import DatabaseExporter


@cli.app.CommandLineApp
def TRAKr(app):
    print "[TRAKr] - Starting Up"
    # make sure the settings are all loaded up and good

    configHelper = ConfigHelper.ConfigHelper()
    configHelper.startUp()

    # handling pre-run parameters first
    if TRAKr.params.reset:
        configHelper.resetConfig()

    if TRAKr.params.export_database:
        DatabaseExporter.exportDatabases()

    # handling run parameters

    if TRAKr.params.scan:
        # root check
        if os.geteuid() == 0:
            # we're good to go, let's scan
            Scanner.beginScan()
        else:
            # too bad
            print "Please run as root to capture packets. Exiting..."
            os._exit(0)


    #giving the params a chance to start their threads
    ThreadKeeper.wait(3)

    ThreadKeeper.waitForThreads()
    print("[TRAKr] - Shutting Down")


# for operational things, use a parameter that gets set
TRAKr.add_param("-r", "--run", help="this starts capture and analysis processing all-in-one. Needs root permissions",
                action='store_true')
TRAKr.add_param("-s", "--scan", help="begin scanning and saving to the database", action='store_true')
TRAKr.add_param("-reset", "--reset", help="resets the config file to defaul", action='store_true')
TRAKr.add_param("-d", "--export_database", help="this exports the graph.db and reduced.db into the /export dir",
                action='store_true', default=False)

if __name__ == '__main__':
    TRAKr.run()

import cli.app
import argparse
import os

from config import ConfigHelper
from scanner import Scanner
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
        # root check, cuz that's needed
        if os.geteuid() == 0:
            Scanner.beginScan()
        else:
            # too bad
            print "Please run as root to capture packets. Exiting..."
            os._exit(0)

    print("[TRAKr] - Shutting Down")


class ExportDatabase(argparse.Action):
    # TODO take in a path for export location
    def __init__(self, option_strings, dest, nargs=None, **kwargs):
        if nargs is not None:
            raise ValueError("nargs not allowed")
        super(ExportDatabase, self).__init__(option_strings, dest, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        print "exporting..."


# actions happen before TRAKr starts, so only use this for resetting config and exporting kinda stuff
# for operational things, use a parameter that gets set

TRAKr.add_param("-r", "--run", help="this starts capture and analysis processing all-in-one. Needs root permissions",
                action='store_true')
TRAKr.add_param("-s", "--scan", help="begin scanning and saving to the database", action='store_true')
TRAKr.add_param("-reset", "--reset", help="resets the config file to defaul", action='store_true')
TRAKr.add_param("-d", "--export_database", help="this exports the graph.db and reduced.db into the /export dir",
                action='store_true', default=False)

if __name__ == '__main__':
    TRAKr.run()

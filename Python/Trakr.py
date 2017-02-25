from config import ConfigHelper
from scanner import Scanner
import cli.app


@cli.app.CommandLineApp
def TRAKr(app):
    print "[TRAKr] - Crowd Analytics"
    # make sure the settings are all loaded up and good

    configHelper = ConfigHelper.ConfigHelper()
    configHelper.startUp()


    print("[TRAKr] - Shutting Down")

#ls.add_param("-l", "--long", help="list in long format", default=False, action="store_true")
TRAKr.add_param("-s", "--scan", help="begin scanning and saving to the database")





if __name__ == '__main__':
    TRAKr.run()
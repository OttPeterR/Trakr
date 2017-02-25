#this loads up the default configurations upon first launch
import ConfigParser
import os


defaultConfigPath = "./trakr.ini"

def createDefaultConfig():
    file = open(defaultConfigPath, 'w')
    config = ConfigParser.ConfigParser()

    fullPath = str(getFullTrakrPath())

    #database section
    config.add_section("db")
    config.set("db", "rolling_path", (fullPath + "/db/rolling.db"))
    config.set("db", "reduced_path", (fullPath + "/db/reduced.db"))
    config.set("db", "graph_path", (fullPath + "/db/graph.db"))

    #monitoring section
    config.add_section("scanner")
    config.set("scanner", "autostart", False)
    config.set("scanner","observation_interval_seconds", 600)

    config.write(file)
    print "Default config created."



def getFullTrakrPath():
    return os.path.dirname(os.path.abspath(__file__))[:-7]
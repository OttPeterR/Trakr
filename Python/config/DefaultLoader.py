#this loads up the default configurations upon first launch
import ConfigParser
import os


defaultConfigPath = "./trakr.ini"

def createDefaultConfig():
    file = open(defaultConfigPath, 'w')
    config = ConfigParser.ConfigParser()

    #database section
    config.add_section("db")
    config.set("db", "rolling_path", (str(getFullTrakrPath()))+"/db/rolling.db")
    config.set("db", "reduced_path", (str(getFullTrakrPath()))+"/db/reduced.db")
    config.set("db", "graph_path", (str(getFullTrakrPath()))+"/db/graph.db")




    #monitoring section
    config.add_section("scanner")
    config.set("scanner","observation_interval_seconds", 600)


    print getFullTrakrPath()

    config.write(file)



def getFullTrakrPath():
    return os.getcwd()[:-7]
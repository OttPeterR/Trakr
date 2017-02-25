import ConfigParser
import DefaultLoader
import os

defaultConfigPath = "./trakr.ini"
config = ConfigParser.ConfigParser()
loaded = False


class ConfigHelper():
    startUp()



#loads up the config file, or a default if its missing
def startUp():
    if loaded:
        return
    reload()



def reload():
    # check if config is missing
    if not os.path.exists(defaultConfigPath):
        # create it if needed
        DefaultLoader.createDefaultConfig()

    # now that we know it's there, load it up
    __loadConfig(defaultConfigPath)


#given the path to the config, load it
def __loadConfig(path):
    global config
    config.read(defaultConfigPath, 'r')
    loaded = True
    return



######################################
########### access methods ###########
######################################

@staticmethod
def getComprehensiveDatabasePath():
    return config.get("db", "comprehensive_path")

@staticmethod
def getReducedDatabasePath():
    return config.get("db", "reduced_path")

@staticmethod
def getGraphDatabasePath():
    return config.get("db", "graph_path")
import ConfigParser
import DefaultLoader
import os


class ConfigHelper():
    global loaded
    global configParser
    global defaultConfigPath

    loaded = False
    configParser = ConfigParser.ConfigParser()

    #loads up the config file, or a default if its missing
    def startUp(self):
        global loaded
        if loaded:
            return
        else:
            self.reloadConfig()




    def reloadConfig(self):
        global configParser

        # check if config is missing
        if not os.path.exists(DefaultLoader.defaultConfigPath):
            # create it if needed
            DefaultLoader.createDefaultConfig()

        # now that we know it's there, load it up
        self.loadConfig()


    #given the path to the config, load it
    def loadConfig(self):
        global configParser
        global loaded

        configParser.read(DefaultLoader.defaultConfigPath)
        loaded = True
        return

    def resetConfig(self):
        DefaultLoader.createDefaultConfig()
        loaded = True


######################################
########### access methods ###########
######################################

    #application

def autoStart():
    return configParser.getboolean("trakr", "autostart")

def getTRAKrFullPath():
    return configParser.get("trakr", "full_path")


    #scanner

def getWirelessCaptureInterface():
    return configParser.get("scanner", "interface")

def getCaptureDuration():
    return configParser.get("scanner", "duration")

    #database

def getRollingDatabasePath():
    return configParser.get("db", "rolling_path")

def getBehaviorDatabasePath():
    return configParser.get("db", "behavior_path")

def getGraphDatabasePath():
    return configParser.get("db", "graph_path")


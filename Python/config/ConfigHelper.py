import ConfigParser
import DefaultLoader
import os


class ConfigHelper():
    #TODO make this a singleton
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

    def autoStart(self):
        return configParser.getboolean("scanner", "autostart")


    #scanner

def getWirelessCaptureInterface():
    return configParser.get("scanner", "interface")

    #database

    def getRollingDatabasePath(self):
        return configParser.get("db", "rolling_path")

    def getBehaviorDatabasePath(self):
        return configParser.get("db", "behavior_path")

    def getGraphDatabasePath(self):
        return configParser.get("db", "graph_path")


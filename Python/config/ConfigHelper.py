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
    defaultConfigPath = "./trakr.ini"

    #loads up the config file, or a default if its missing
    def startUp(self):
        global loaded
        if loaded:
            return
        else:
            self.reloadConfig()




    def reloadConfig(self):
        global configParser
        global defaultConfigPath

        # check if config is missing
        if not os.path.exists(defaultConfigPath):
            # create it if needed
            DefaultLoader.createDefaultConfig()

        # now that we know it's there, load it up
        self.loadConfig()


    #given the path to the config, load it
    def loadConfig(self):
        global configParser
        global defaultConfigPath
        global loaded

        configParser.read(defaultConfigPath)
        loaded = True
        return





######################################
########### access methods ###########
######################################

    def getRollingDatabasePath(self):
        return configParser.get("db", "rolling_path")

    def getReducedDatabasePath(self):
        return configParser.get("db", "reduced_path")

    def getGraphDatabasePath(self):
        return configParser.get("db", "graph_path")

    def autoStart(self):
        return configParser.getboolean("scanner", "autostart")
import ConfigParser
import DefaultConfigLoader
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
        if not os.path.exists(DefaultConfigLoader.defaultConfigPath):
            # create it if needed
            DefaultConfigLoader.createDefaultConfig()

        # now that we know it's there, load it up
        self.loadConfig()


    #given the path to the config, load it
    def loadConfig(self):
        global configParser
        global loaded

        configParser.read(DefaultConfigLoader.defaultConfigPath)
        loaded = True
        return

    def resetConfig(self):
        DefaultConfigLoader.createDefaultConfig()
        loaded = True


######################################
########### access methods ###########
######################################


    #application

def autoStart():
    return configParser.getboolean("trakr", "autostart")

def getTRAKrFullPath():
    return configParser.get("trakr", "full_path")

def getKey():
    return configParser.get("trakr", "key")



    #scanner

def getWirelessCaptureInterface():
    return configParser.get("scanner", "interface")

def getCaptureDuration():
    return configParser.get("scanner", "duration")

def getCaptureDirectory():
    return configParser.get("scanner", "capture_dir")

def getKeepAllPcaps():
    return configParser.getboolean("scanner", "keep_all_pcap")


    #database

def getRollingDatabasePath():
    return configParser.get("db", "rolling_path")

def getBehaviorDatabasePath():
    return configParser.get("db", "behavior_path")

def getGraphDatabasePath():
    return configParser.get("db", "graph_path")

def shouldHash():
    return configParser.getboolean("db", "hash_values")


    # analysis

def getEntryTime():
    return configParser.get("analysis", "entry_time")

def getExitTime():
    return configParser.get("analysis", "exit_time")

def getHourSegments():
    return configParser.get("analysis", "seg_per_hour")

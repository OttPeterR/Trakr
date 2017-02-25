import ConfigParser
import DefaultLoader
import os

defaultConfigPath = "trakr.cfg"

config = ConfigParser.ConfigParser()

#loads up the config file, or a default if its missing
def startUp():
    #check if config is missing
    if not os.path.exists(defaultConfigPath):
        #create it if needed
        DefaultLoader.createDefaultConfig()

    #now that we know it's there, load it up
    __loadConfig(defaultConfigPath)

#given the path to the config, load it
def __loadConfig(path):
    global config
    config.read(defaultConfigPath)
    return


#this loads up the default configurations upon first launch
import ConfigParser

defaultConfigPath = "./trakr.ini"

def createDefaultConfig():
    file = open(defaultConfigPath, 'w')
    config = ConfigParser.ConfigParser()
    config.write(file)




createDefaultConfig()
#this loads up the default configurations upon first launch
import ConfigParser
import os


defaultConfig = "/trakr.ini"

def createDefaultConfig():

    fullPath = __getFullTrakrPath()

    file = open(getConfigPath(), 'w')
    config = ConfigParser.ConfigParser()

    config.add_section("trakr")
    config.set("trakr", "full_path", fullPath)
    config.set("trakr", "autostart", False)
    config.set("trakr", "key", "you-need-to-change-this")

    # database section
    config.add_section("db")
    config.set("db", "rolling_path", (fullPath + "/runtime/db/rolling.db"))
    config.set("db", "behavior_path", (fullPath + "/runtime/db/behavior.db"))
    config.set("db", "graph_path", (fullPath + "/runtime/db/graph.db"))
    config.set("db", "hash_values", True)

    # scanner section
    config.add_section("scanner")
    # TODO
    # find a way to check the OS and then get the default interface
    # because this works for MacOS only
    config.set("scanner", "interface", "en0")
    config.set("scanner","duration", 60*10) #scan for 10 minutes
    config.set("scanner", "capture_dir", fullPath+"/runtime/pcap/")
    config.set("scanner", "keep_all_pcap", False)


    # analysis section
    config.add_section("analysis")
    config.set("analysis", "exit_time", 60*45) # 45 minutes
    config.set("analysis", "entry_time", 60*5) # 6 minutes
    config.set("analysis", "seg_per_hour", 6) # 6 per hour = 10 minute blocks
    config.set("analysis", "back_track_hours", 3) # will look backwards 3 hours into the db for behavior analysis


    config.write(file)
    print "Default config written."



def __getFullTrakrPath():
    return os.path.dirname(os.path.abspath(__file__))[:-7]

def getConfigPath():
    fullPath = str(__getFullTrakrPath())
    defaultConfigPath = fullPath + defaultConfig
    return defaultConfigPath
#this loads up the default configurations upon first launch
import ConfigParser
import os


defaultConfigPath = "./trakr.ini"

def createDefaultConfig():
    file = open(defaultConfigPath, 'w')
    config = ConfigParser.ConfigParser()

    fullPath = str(getFullTrakrPath())


    config.add_section("trakr")
    config.set("trakr", "full_path", fullPath)
    config.set("trakr", "autostart", False)


    #database section
    config.add_section("db")
    config.set("db", "rolling_path", (fullPath + "/db/rolling.db"))
    config.set("db", "behavior_path", (fullPath + "/db/behavior.db"))
    config.set("db", "graph_path", (fullPath + "/db/graph.db"))

    #monitoring section
    config.add_section("scanner")
    # TODO
    # find a way to check the OS and then get the default interface
    # because this works for MacOS only
    config.set("scanner", "interface", "en0")
    config.set("scanner","duration", 15)

    #analysis section
    config.add_section("analysis")
    config.set("analysis", "exit_seconds", 1800) # 30 minutes
    config.set("analysis", "enter_period_seconds", 180)

    # enter_period_second will be divided into enter_subperiod groups
    # and there must be at least one wifi observation in each of those
    # groups to then assume the person has entered and is not just passing by
    config.set("analysis", "enter_subperiods", 4)



    config.write(file)
    print "Default config written."



def getFullTrakrPath():
    return os.path.dirname(os.path.abspath(__file__))[:-7]
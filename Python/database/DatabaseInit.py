import sqlite3
from subprocess import call
from config import ConfigHelper

def initDBs():
    __initDB(ConfigHelper.getRollingDatabasePath())
    __initDB(ConfigHelper.getBehaviorDatabasePath())
    #TODO init graph database
    print "Databases initialized."
    return


def __initDB(path):
    call(["touch", path])
    call(["chmod", "777", path])
    connection = sqlite3.connect(path)
    connection.close()
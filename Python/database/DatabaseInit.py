import sqlite3
from subprocess import call
from config import ConfigHelper
from database.relational import RollingDatabaseHelper
from database.relational import BehaviorDatabaseHelper


def initDBs():
    __initDB(ConfigHelper.getRollingDatabasePath())
    RollingDatabaseHelper.init()

    __initDB(ConfigHelper.getBehaviorDatabasePath())
    BehaviorDatabaseHelper.init()

    #TODO init graph database
    #print "Databases initialized."
    return

def deleteDBs():
    __deleteDB(ConfigHelper.getRollingDatabasePath())
    __deleteDB(ConfigHelper.getBehaviorDatabasePath())
    print "Databases deleted."


def __initDB(path):
    call(["touch", path])
    call(["chmod", "644", path])
    connection = sqlite3.connect(path)
    connection.close()


def __deleteDB(path):
    call(["rm", path])

from config import ConfigHelper
from database import PrivacyUtility
import sqlite3

create_reduced_db = "CREATE TABLE IF NOT EXISTS %s \
               (ID INT PRIMARY KEY     NOT NULL, \
               ADDRESS         TEXT    NOT NULL, \
               TIME            DOUBLE  NOT NULL, \
               TYPE            SHORT   NOT NULL, \
               LAT             DOUBLE  NOT NULL, \
               LONG            DOUBLE  NOT NULL);"

create_behavior_db = "CREATE TABLE IF NOT EXISTS %s\
               (ADDRESS   TEXT   PRIMARY KEY   NOT NULL);"


get_all_macs = "SELECT ADDRESS FROM %s"
insert_command = "INSERT INTO %s (ADDRESS) VALUES ('%s')"

def init():
    connect()
    __behavioralDatabaseInit()

def loadObservation(mac, time, type):
    global connection
    #adds in the data to the table

    return

def connect():
    global connection
    pathToDB = ConfigHelper.getBehaviorDatabasePath()
    connection = sqlite3.connect(pathToDB)

def commit():
    global connection
    connection.commit()

def close():
    global connection
    connection.close()

#this makes the database if it does not exist
def __behavioralDatabaseInit():
    global connection

    #making table for the behaviors of when they enter and exit
    connection.execute(create_reduced_db % ConfigHelper.getReducedTableName())

    #making table to hold all unique MACs
    connection.execute(create_behavior_db % ConfigHelper.getUniqueTableName())
    commit()


#True - if the address was successfully stored or it was ignored
#False - if there was a problem storing the address
def addNewAddress(address):
    global connection
    try:
        connection.execute(insert_command % (str(ConfigHelper.getUniqueTableName()), address))
    except Exception, errmsg:
        #print "New MAC address not inserted, was not unique"
        #print errmsg
        #I'll just let it handle uniqueness checking, maybe fix this if it gets slow
        return False
    return True


def getUniques():
    global connection

    cursor = connection.execute(get_all_macs % str(ConfigHelper.getUniqueTableName()))
    macs = []
    for c in cursor:
        macs.append(c[0])

    return macs
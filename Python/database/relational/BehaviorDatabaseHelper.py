
from config import ConfigHelper
from database import PrivacyUtility
import sqlite3


def init():
    connect()
    __behavioralDatabaseInit()

def loadObservation(mac, time, type):
    global connection
    #adds in the data to the table

    return



#this makes the database if it does not exist
def __behavioralDatabaseInit():
    global connection

    #making table for the behaviors of when they enter and exit
    connection.execute("CREATE TABLE IF NOT EXISTS "+str(ConfigHelper.getReducedTableName())+" \
               (ID INT PRIMARY KEY     NOT NULL, \
               ADDRESS         TEXT    NOT NULL, \
               TIME            INT     NOT NULL, \
               TYPE            SHORT   NOT NULL, \
               LAT             DOUBLE  NOT NULL, \
               LONG            DOUBLE  NOT NULL);")

    #making table to hold all unique MACs
    connection.execute("CREATE TABLE IF NOT EXISTS "+str(ConfigHelper.getUniqueTableName())+ "\
               (ADDRESS   TEXT   PRIMARY KEY   NOT NULL);")

    #adding in the default addresses to the top of the DB
    default_addresses = ["000000000000", "error", "nothing"]
    for addr in default_addresses:
        if ConfigHelper.shouldHash():
            addNewAddress(PrivacyUtility.hash(addr))
        else:
            addNewAddress(addr)


    commit()


#True - if the address was successfully stored or it was ignored
#False - if there was a problem storing the address
def addNewAddress(address):
    global connection
    try:

        connection.execute("INSERT INTO "+str(ConfigHelper.getUniqueTableName())+" (ADDRESS) VALUES ('"+address+"')");

    except Exception, errmsg:
        #print "New MAC address not inserted, was not unique"
        #print errmsg

        #I'll just let it handle uniqueness checking, maybe fix this if it gets slow
        return False
    return True

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
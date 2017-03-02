
from config import ConfigHelper
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
    connection.execute('''CREATE TABLE IF NOT EXISTS REDUCED
               (ID INT PRIMARY KEY     NOT NULL,
               ADDRESS         TEXT    NOT NULL,
               TIME            INT     NOT NULL,
               TYPE            SHORT   NOT NULL,
               LAT             DOUBLE  NOT NULL,
               LONG            DOUBLE  NOT NULL);''')

    #making table to hold all unique MACs
    connection.execute('''CREATE TABLE IF NOT EXISTS UNIQUEMACS
               (ADDRESS     TEXT     PRIMARY KEY     NOT NULL);''')
    addNewAddress("None")
    commit()



def addNewAddress(address):
    global connection
    try:
        connection.execute("INSERT INTO UNIQUEMACS (ADDRESS) VALUES ('"+str(address)+"')");
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
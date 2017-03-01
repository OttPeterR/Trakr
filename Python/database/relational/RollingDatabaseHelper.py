from config import ConfigHelper
import sqlite3


def init():
    global connection

    pathToDB = ConfigHelper.getRollingDatabasePath()
    connection = sqlite3.connect(pathToDB)
    __rollingDatabaseInit()

def loadPacket(packet):
    global connection
    #loads it into the database

    #the type of packet is Observationd

    return True


#this makes the database if it does not exist
def __rollingDatabaseInit():
    global connection
    connection.execute('''CREATE TABLE IF NOT EXISTS ROLLING
           (ID INT PRIMARY KEY     NOT NULL,
           ADDRESS         TEXT    NOT NULL,
           TIME            INT     NOT NULL,
           LAT             DOUBLE  NOT NULL,
           LONG            DOUBLE  NOT NULL);''')
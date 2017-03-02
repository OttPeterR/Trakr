from config import ConfigHelper
import sqlite3


def init():
    global connection

    connect()
    __rollingDatabaseInit()

def loadPacket(o):
    global connection
    #the type of packet is Observation
    connection.execute("INSERT INTO OBSERVATIONS (ADDRESS, TIME, LAT, LONG) \
                            VALUES ("
                                " '"+str(o.mac)+"' , "
                                +str(o.time)+", "
                                +str(o.lat)+", "
                                +str(o.long)+" )")


    return True


#this makes the database if it does not exist
def __rollingDatabaseInit():
    global connection

    #(ID INT PRIMARY KEY     NOT NULL, \

    connection.execute("CREATE TABLE IF NOT EXISTS OBSERVATIONS \
           (ADDRESS        TEXT    NOT NULL, \
           TIME            DOUBLE  NOT NULL, \
           LAT             DOUBLE  NOT NULL, \
           LONG            DOUBLE  NOT NULL);")
    commit()

def connect():
    global connection
    pathToDB = ConfigHelper.getRollingDatabasePath()
    connection = sqlite3.connect(pathToDB)

def commit():
    global connection
    connection.commit()

def close():
    global connection
    connection.close()

from config import ConfigHelper
import sqlite3


class RollingDatabaseHelper():
    global conn

    pathToDB = ConfigHelper.getRollingDatabasePath()
    #open connection with database
    conn =sqlite3.connect(pathToDB)


def loadObservation(mac, time, type):
    global conn
    #adds in the data to the table

    return



#this makes the database if it does not exist
def rollingDatabaseInit():
    conn.execute('''CREATE TABLE REDUCED
           (ID INT PRIMARY KEY     NOT NULL,
           ADDRESS         TEXT    NOT NULL,
           TIME            INT     NOT NULL,
           TYPE            SHORT   NOT NULL,
           LAT             DOUBLE  NOT NULL,
           LONG            DOUBLE  NOT NULL);''')
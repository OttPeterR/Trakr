from config import ConfigHelper
import sqlite3


class RollingDatabaseHelper():
    global conn

    pathToDB = ConfigHelper.getRollingDatabasePath()
    #open connection with database
    conn =sqlite3.connect(pathToDB)


def loadPacket(mac, time):
    global conn
    #loads it into the database

    return True


#this makes the database if it does not exist
def rollingDatabaseInit():
    conn.execute('''CREATE TABLE ROLLING
           (ID INT PRIMARY KEY     NOT NULL,
           ADDRESS         TEXT    NOT NULL,
           TIME            INT     NOT NULL);''')
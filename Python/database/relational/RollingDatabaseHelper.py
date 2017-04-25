from config import ConfigHelper
import sqlite3
from database import PrivacyUtility
from file.pcap import Observation

table = "OBSERVATIONS"
rolling_table_creation = "CREATE TABLE IF NOT EXISTS " + table + " \
           (ADDRESS        TEXT    NOT NULL, \
           TIME            LONG  NOT NULL, \
           LAT             DOUBLE  NOT NULL, \
           LONG            DOUBLE  NOT NULL);"
get_observations_of_address = "SELECT TIME FROM " + table + " WHERE ADDRESS==\"%s\""
get_observations_between_times = "SELECT * FROM " + table + " WHERE TIME>=%s AND TIME<=%s"
insert_command = "INSERT INTO " + table + " (ADDRESS, TIME, LAT, LONG) VALUES ('%s', %s, %s, %s)"
remove_bad_packets = "DELETE FROM " + table + " WHERE ADDRESS == '%s'"


def init():
    conn = connect()
    __rollingDatabaseInit(conn)


def connect():
    pathToDB = ConfigHelper.getRollingDatabasePath()
    connection = sqlite3.connect(pathToDB)
    return connection


def commit(connection):
    connection.commit()


def close(connection):
    connection.close()


def loadPacket(connection, o):
    # the type of packet is Observation

    addr = PrivacyUtility.processAddress(o.mac)
    connection.execute(insert_command % (addr, str(o.time), str(o.lat), str(o.long)))
    return True


def removeBadPackets(connection):
    for bad in Observation.bad_addresses:
        # might have to hash them if config says so
        if ConfigHelper.shouldHash():
            bad = PrivacyUtility.processAddress(bad)
        connection.execute(remove_bad_packets % bad)
    connection.commit()


# this makes the database if it does not exist
def __rollingDatabaseInit(connection):
    # (ID INT PRIMARY KEY     NOT NULL, \

    connection.execute(rolling_table_creation)
    connection.commit()


def getTimesOfAddress(connection, address):
    cursor = connection.execute(get_observations_of_address % address)
    obs = []
    last = 0
    for c in cursor:
        # adding values that are not the same as the previous;y added one
        # this cuts down on duplicate observations in the same second
        val = int(c[0])
        if val != last:
            obs.append(val)
        last = val
    return obs

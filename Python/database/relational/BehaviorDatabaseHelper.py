import sqlite3

from config import ConfigHelper
from file.pcap import Observation
from database import PrivacyUtility

table_reduced = "REDUCED"
table_unique = "UNIQUEMACS"
table_usercount = "USERCOUNT"

type_exit = 0b0  # also means for "not present" sometimes
type_notice = 0b1
type_enter = 0b10

create_reduced_db = "CREATE TABLE IF NOT EXISTS " + table_reduced + " \
               (ADDRESS         TEXT    NOT NULL, \
               TIME            LONG  NOT NULL, \
               TYPE            SHORT   NOT NULL, \
               LAT             DOUBLE  NOT NULL, \
               LONG            DOUBLE  NOT NULL);"
create_unique_db = "CREATE TABLE IF NOT EXISTS " + table_unique + "\
               (ADDRESS   TEXT   PRIMARY KEY   NOT NULL," \
                "TIME       INT                 NOT NULL);"
create_usercount_db = "CREATE TABLE IF NOT EXISTS " + table_usercount + "" \
                                                                        "(TIME    LONG  NOT NULL," \
                                                                        "NUM_USERS    INT     NOT NULL)"
# unique MACs
get_all_macs_after = "SELECT ADDRESS FROM " + table_unique+" WHERE TIME >= %s"
insert_unique_command = "INSERT INTO " + table_unique + " (ADDRESS, TIME) VALUES ('%s', %s)"
update_unique_command = "UPDATE "+table_unique+" SET TIME=%s WHERE ADDRESS=='%s' "

# reduced db commands
insert_behavior = "INSERT INTO " + table_reduced + "(ADDRESS, TIME, TYPE, LAT, LONG) VALUES ('%s', %s, %s, %s, %s)"
get_last_observation = "SELECT TYPE FROM (SELECT MAX(TIME), TYPE FROM " + table_reduced + " WHERE ADDRESS=='%s')"
# getting al obs of the specified address, then sorting by their time
get_all_action_for_address = "SELECT TYPE, TIME FROM (SELECT TYPE, TIME FROM " + table_reduced + " WHERE ADDRESS == '%s') ORDER BY TIME ASC"


def init():
    conn = connect()
    __behavioralDatabaseInit(conn)


def loadObservation(connection, mac, time, type):
    # TODO:adds in the data to the table

    return


def connect():
    pathToDB = ConfigHelper.getBehaviorDatabasePath()
    connection = sqlite3.connect(pathToDB)
    return connection


def commit(connection):
    connection.commit()


def close(connection):
    connection.close()


# this makes the database if it does not exist
def __behavioralDatabaseInit(connection):
    # makign table to hold how many users are currently present for an interval
    connection.execute(create_usercount_db)
    # making table to hold all unique MACs
    connection.execute(create_unique_db)
    # making table for the behaviors of when they enter and exit
    connection.execute(create_reduced_db)

    # adding in the default MACs that are not needed
    __addPresetAddresses(connection)

    connection.commit()


def __addPresetAddresses(connection):
    for addr in Observation.bad_addresses:
        addNewAddress(connection, addr)
    return


# True - if the address was successfully stored or it was ignored
# False - if there was a problem storing the address
def addNewAddress(connection, address, time=0):
    try:
        address = PrivacyUtility.processAddress(address)
        connection.execute(insert_unique_command % (address, time))
        connection.commit()
        return True
    except Exception:
        #maybe it was already in there, so lets try updating it instead
        try:
            connection.execute(update_unique_command % (time, address))
            return True
        except Exception:
            pass
    return False



def getUniques(connection, startTime):
    cursor = connection.execute(get_all_macs_after % startTime)
    macs = []
    for c in cursor:
        macs.append(c[0])
    return macs


def addBehavior(connection, address, type, time, lat, long):
    # remember to commit the connection after doing this
    # it doesnt automatically commit on its own because this can get called rapidly
    connection.execute(insert_behavior % (address, time, type, lat, long))


def getMostRecentStatus(connection, address):
    cursor = connection.execute(get_last_observation % address)
    result = type_exit
    # TODO this is bad, please fix me
    for c in cursor:
        result = c[0]
    return result


def getAllActionsForAddress(connection, address):
    cursor = connection.execute(get_all_action_for_address % address)
    actions = []
    for c in cursor:
        # TYPE, TIME
        actions += [(c[0], c[1])]
    return actions

from database.relational import RollingDatabaseHelper, BehaviorDatabaseHelper

def processObservations(observations):
    conn_rolling = RollingDatabaseHelper.connect()
    conn_behavior = BehaviorDatabaseHelper.connect()

    __loadObservations(conn_rolling, observations)
    RollingDatabaseHelper.removeBadPackets(conn_rolling)
    __getUniqueMACs(conn_behavior, observations)

    conn_rolling.close()
    conn_behavior.close()



def __loadObservations(connection, observations):
    for o in observations:
        RollingDatabaseHelper.loadPacket(connection, o)
    connection.commit()
    return


def __getUniqueMACs(connection, observations):
    ind = 0
    newUnique = 0
    dict = {}  # dictionary of unique MAC addresses
    address = ""
    for o in observations:
        # is this a new mac address?
        if o.mac not in dict:
            dict[o.mac] = ind
            if BehaviorDatabaseHelper.addNewAddress(connection, o.mac, o.time):
                newUnique = newUnique + 1
            ind = ind + 1
            print "{0}\r".format("  new devices: " + str(newUnique)),
    print
    return
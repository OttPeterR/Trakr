import time
from database.relational import RollingDatabaseHelper
from database.relational import BehaviorDatabaseHelper
from config import ConfigHelper


# this class parses over all the data taken direcly from the pcap files
# it iterates on addresses and creates the entry and exit actions

def analyze():
    global action_exit, action_notice
    action_notice = BehaviorDatabaseHelper.type_notice
    action_exit = BehaviorDatabaseHelper.type_exit

    behaviorDBConnection = BehaviorDatabaseHelper.connect()
    rollingDBConnection = RollingDatabaseHelper.connect()

    # current GMT minus the backtracking time (in seconds)

    startTime = int(time.time()) - int(
        ConfigHelper.getCaptureDuration())  # int(ConfigHelper.getNumBackTrackHours() * 3600)
    # or if we want to analyze everything we've ever captured
    if ConfigHelper.doAllAnalysisForever():
        startTime = 0

    uniques = BehaviorDatabaseHelper.getUniques(behaviorDBConnection, startTime)

    count = 0
    total = len(uniques)
    for address in uniques:
        count += 1
        print '{0}\r'.format("  analysis: " + str(100 * count / total) + "%"),

        # array of int
        timesOfAddress = RollingDatabaseHelper.getTimesOfAddress(rollingDBConnection, address)

        makeEntriesAndExitsForAddress(address, timesOfAddress, behaviorDBConnection)

    # make a new line to advance from the percentage print output
    print

    # commit changes to behavior db and close out both connections
    behaviorDBConnection.commit()
    behaviorDBConnection.close()
    rollingDBConnection.close()
    return


def makeEntriesAndExitsForAddress(address, times, behaviorDB):
    global action_exit, action_notice

    observation_actions = []  # this will hold the entry/exit actions

    if len(times) > 0:

        # if there was a previous observation, let's find it
        previous = -1
        lastKnown = __loadLastKnownState(behaviorDB, address)
        if lastKnown is not None:
            previous = lastKnown
            # if the last observation was a leave and it should be, this'll fix it
            __fixPreviousAction(behaviorDB, address, previous, times[0])

        time_difference = 0
        for cur_time in times:
            time_difference = cur_time - previous

            # find what the state is of the current observation, based on the previous

            # Did the device leave since we last saw it?
            if time_difference > ConfigHelper.getExitTime():
                # so the previous one was an exit
                if (previous != -1):
                    observation_actions += [(action_exit, previous)]

                # and it was just seen entering
                observation_actions += [(action_notice, cur_time)]

                # else, its just another observation, we don't care too much about it

            # update previous
            previous = cur_time

        # make the last observation a leave, it'll get updated if it actually isn't
        observation_actions += [(action_exit, previous)]

    else:
        # no observations --> nothing to do, move along
        return

    # putting the observations into the behavior database
    for actions in observation_actions:
        # actions is a tuple
        BehaviorDatabaseHelper.addBehavior(behaviorDB, address, actions[0],
                                           actions[1])  # can add lat/long here if you want


def makeTimeSlots():
    # returns an array of the size of time slots that should be created
    slotsPerHour = ConfigHelper.getHourSegments()
    backTrackHours = ConfigHelper.getNumBackTrackHours()
    return [0] * slotsPerHour * backTrackHours


def __loadLastKnownState(connection, addr):
    return BehaviorDatabaseHelper.getMostRecentStatus(connection, addr)


def __fixPreviousAction(connection, address, previousTime, newTime):
    # should it be removed?
    if newTime - previousTime < ConfigHelper.getExitTime():
        BehaviorDatabaseHelper.removeFalseExit(connection, address, previousTime)
        pass
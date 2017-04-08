import time
from database.relational import RollingDatabaseHelper
from database.relational import BehaviorDatabaseHelper
from config import ConfigHelper


def analyze():
    global action_exit, action_notice
    action_notice = BehaviorDatabaseHelper.type_notice
    action_exit = BehaviorDatabaseHelper.type_exit

    behaviorDBConnection = BehaviorDatabaseHelper.connect()
    rollingDBConnection = RollingDatabaseHelper.connect()

    # current GMT minus the backtracking time (in seconds)

    startTime = int(time.time()) - int(ConfigHelper.getCaptureDuration())#int(ConfigHelper.getNumBackTrackHours() * 3600)
    # or if we want to analyze everything we've ever captured
    if ConfigHelper.doAllAnalysisForever():
        startTime = 0

    uniques = BehaviorDatabaseHelper.getUniques(behaviorDBConnection, startTime)
    timeSlots = makeTimeSlots()

    print "num uniques: "+str(len(uniques))
    count = 0
    total = len(uniques)
    for address in uniques:
        count += 1
        observationsOfAddress = RollingDatabaseHelper.getObservationsOfAddress(rollingDBConnection, address)

        makeEntriesAndExitsForAddress(address, observationsOfAddress, behaviorDBConnection, rollingDBConnection)

        # now that entries and exits have been made for this address
        # parse through each one and find if they were present during
        # the interval specified by the config

        # getting all actions for this address (there could be other ones in
        # the DB that were not in this capture)
        actions = BehaviorDatabaseHelper.getAllActionsForAddress(behaviorDBConnection, address)

        #if len(actions) > 1:
        #    for action in actions:
        #        # each action is a tuple of (TYPE, TIME)
        #        continue

        print '{0}\r'.format("  analysis: " + str(100 * count / total) + "%"),
    print

    # commit changes to behavior db and close out both connections
    behaviorDBConnection.commit()
    behaviorDBConnection.close()
    rollingDBConnection.close()
    return


def makeEntriesAndExitsForAddress(address, observations, behaviorDB, rollingDB):
    global action_exit, action_notice

    observation_actions = []  # this will hold the entry/exit actions

    if len(observations) > 1:

        previous_state = __loadState(behaviorDB, address)
        #print "new device:"
        for o in range(1, len(observations)):
            dist = observations[o].time - observations[o - 1].time

            # find what the state is of the current observation, based on the previous

            # how long has it been since last seeing this device?
            if dist > ConfigHelper.getExitTime():
                observation_actions += [(action_exit, observations[o - 1].time)]
                #print "exit: " + str(observations[o - 1].time)

                observation_actions += [(action_notice, observations[o].time)]
                #print "enter: " + str(observations[o].time)


    elif len(observations) == 1:
        # there is only one observation, just handle it as a notice
        observation_actions += [(action_notice, observations[0].time)]
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


def __loadState(connection, addr):
    return BehaviorDatabaseHelper.getMostRecentStatus(connection, addr)

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
    startTime = int(time.time()) - int(ConfigHelper.getNumBackTrackHours() * 3600)
    # or if we want to analyze everything we've ever captured
    if ConfigHelper.doAllAnalysisForever():
        startTime = 0

    uniques = BehaviorDatabaseHelper.getUniques(behaviorDBConnection, startTime)
    timeSlots = makeTimeSlots()

    print len(uniques)

    for address in uniques:
        observationsOfAddress = RollingDatabaseHelper.getObservationsOfAddress(rollingDBConnection, address)

        makeEntriesAndExitsForAddress(address, observationsOfAddress, behaviorDBConnection, rollingDBConnection)

        # now that entries and exits have been made for this address
        # parse through each one and find if they were present during
        # the interval specified by the config

        # getting all actions for this address (there could be other ones in
        # the DB that were not in this capture)
        actions = BehaviorDatabaseHelper.getAllActionsForAddress(behaviorDBConnection, address)

        if len(actions) > 1:
            for action in actions:
                # each action is a tuple of (TYPE, TIME)
                continue

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

        for o in range(len(observations) - 1):
            dist = observations[o + 1].time - observations[o].time

            # find what the state is

            if dist > 30:  # ConfigHelper.getExitTime():
                current_state = action_notice
            else:
                current_state = action_exit

            # check if a new state change needs to be added to the list
            if current_state == action_notice and previous_state == action_exit:
                observation_actions += [(action_notice, observations[o + 1].time)]
            elif current_state == action_exit and previous_state == action_notice:
                observation_actions += [(action_exit, observations[o].time)]
                observation_actions += [(action_notice, observations[0 + 1].time)]
                o = o + 1

            # make the current state usable for next iteration
            previous_state = current_state

    elif len(observations) == 1:
        # there is only one observation, just handle it as a notice
        observation_actions += [(action_notice, observations[0].time)]
    else:
        # no observations --> nothing to do, move along
        return

    # putting the observations into the behavior database
    for actions in observation_actions:
        # actions is a tuple
        BehaviorDatabaseHelper.addBehavior(behaviorDB, address, actions[0], actions[1], 0, 0)


def makeTimeSlots():
    # returns an array of the size of time slots that should be created
    slotsPerHour = ConfigHelper.getHourSegments()
    backTrackHours = ConfigHelper.getNumBackTrackHours()
    return [0] * slotsPerHour * backTrackHours


def __loadState(connection, addr):
    return BehaviorDatabaseHelper.getMostRecentStatus(connection, addr)


def test():
    ConfigHelper.ConfigHelper().startUp()
    analyze()


test()

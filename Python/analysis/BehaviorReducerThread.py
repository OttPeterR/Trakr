from database.relational import RollingDatabaseHelper
from database.relational import BehaviorDatabaseHelper
from config import ConfigHelper


def analyze():
    global action_exit, action_notice

    # parses through the rolling database and makes guesses as to when MACs enter and exit
    # after computation, it gives its data to the BehaviorDatabase to insert it into the DB

    # naive solution

    # m loop unique MACs
    # boolean flags as to the status of m, notice -> enter -> present -> exit -> repeat
    # get all from db where MAC = m and put it in an array
    # loop through that array ^ and add labels to the items of notice, enter, present, exit
    # reduce the array by taking out all "present" items that are between present items

    behaviorDBConnection = BehaviorDatabaseHelper.connect()
    rollingDBConnection = RollingDatabaseHelper.connect()

    uniques = BehaviorDatabaseHelper.getUniques(behaviorDBConnection)

    action_notice = BehaviorDatabaseHelper.type_notice
    action_exit = BehaviorDatabaseHelper.type_exit

    for address in uniques:
        observationsOfAddress = RollingDatabaseHelper.getObservationsOfAddress(rollingDBConnection, address)

        reduceBehaviorsForAddress(address, observationsOfAddress, behaviorDBConnection, rollingDBConnection)

    # commit changes to behavior db and close out connections
    behaviorDBConnection.commit()
    behaviorDBConnection.close()
    rollingDBConnection.close()
    return


def reduceBehaviorsForAddress(address, observations, behaviorDB, rollingDB):
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


def __loadState(connection, addr):
    return BehaviorDatabaseHelper.getMostRecentStatus(connection, addr)


def test():
    ConfigHelper.ConfigHelper().startUp()
    analyze()


test()

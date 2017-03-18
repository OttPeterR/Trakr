from database.relational import RollingDatabaseHelper
from database.relational import BehaviorDatabaseHelper
from config import ConfigHelper

def analyze():
    # parses through the rolling database and makes guesses as to when MACs enter and exit
    # after computation, it gives its data to the BehaviorDatabase to insert it into the DB

    # naive solution

    # m loop unique MACs
    # boolean flags as to the status of m, notice -> enter -> present -> exit -> repeat
    # get all from db where MAC = m and put it in an array
    # loop through that array ^ and add labels to the items of notice, enter, present, exit
    # reduce the array by taking out all "present" items that are between present items

    behaviorDB = BehaviorDatabaseHelper.connect()
    rollingDB = RollingDatabaseHelper.connect()

    uniques = BehaviorDatabaseHelper.getUniques(behaviorDB)
    action_notice = 0b1
    action_exit = 0b0

    for u in uniques:
        observations = RollingDatabaseHelper.getObservationsOfAddress(rollingDB, u)
        observation_actions = []  # this will hold the entry/exit actions

        if len(observations) > 1:

            previous_state = __loadState(u)

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

                # make the current state usable for next iteration
                previous_state = current_state
        elif len(observations) == 1:
            # there is only one observation, just handle it as a notice
            observation_actions += [(action_notice, observations[0].time)]
        else:
            # no observations: nothing to do, move along to the next iteration
            continue

    behaviorDB.close()
    rollingDB.close()
    return


def __loadState(addr):
    # TODO: load state from possible previous observations in reducedDB
    return 0b0


def test():
    ConfigHelper.ConfigHelper().startUp()
    analyze()


test()

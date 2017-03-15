from database.relational import RollingDatabaseHelper
from database.relational import BehaviorDatabaseHelper
from config import ConfigHelper

state_not_present = 0b0
state_noticed = 0b01
state_present = 0b10


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

    # declaring vars for state tracking

    current_state = 0  # the current state of the mac, noticed, present, not present
    begining_observation = 0  # the first notice or the first notice after a declared exit
    # this is the first of the entry markers
    observation_segments = []  # this will hold the markers

    observations = []
    for u in uniques:
        observations = RollingDatabaseHelper.getObservationsOfAddress(rollingDB, u)
        if len(observations) > 0:

            state = __loadState(u)
            biggest_separation = 0
            dist = 0

            # now loop through observations and see when they come and go
            for o in range(len(observations) - 1):
                dist = observations[o + 1].time - observations[o].time
                if dist > biggest_separation:
                    biggest_separation = dist

            print "%s %s\t\t%s" % (len(observations), biggest_separation, u)

    behaviorDB.close()
    rollingDB.close()
    return


def __loadState(addr):
    # TODO: load state from possible previous observations in reducedDB
    return state_not_present


def test():
    ConfigHelper.ConfigHelper().startUp()
    analyze()


test()

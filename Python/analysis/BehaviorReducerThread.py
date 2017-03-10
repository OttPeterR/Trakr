from database.relational import RollingDatabaseHelper
from database.relational import BehaviorDatabaseHelper
from config import ConfigHelper

def analyze():
    # parses through the rolling database and makes guesses as to when MACs enter and exit
    # after computation, it gives its data to the BehaviorDatabase to insert it into the DB

    #naive solution

    # m loop unique MACs
        # boolean flags as to the status of m, notice -> enter -> present -> exit -> repeat
        # get all from db where MAC = m and put it in an array
        # loop through that array ^ and add labels to the items of notice, enter, present, exit
        # reduce the array by taking out all "present" items that are between present items


    uniques = BehaviorDatabaseHelper.getUniques()

    observations = []
    for u in uniques:
        observations = RollingDatabaseHelper.getObservationsOfAddress(u)
        # now loop through observations and see when they come and go
    return
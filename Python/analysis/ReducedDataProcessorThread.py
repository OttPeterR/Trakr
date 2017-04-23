from database.relational import BehaviorDatabaseHelper
from config import ConfigHelper

# this class will parse through a sorted list of all observations and create a large array of data to be written to output
# puts data into usercount table of behaviorDB

def export():
    # this is a 2d array of the rows to be exported
    csv_data = [[]]

    conn = BehaviorDatabaseHelper.connect()
    all_actions = BehaviorDatabaseHelper.getAllActionsSortedbyTime(conn)

    index = 0
    len = len(all_actions)

    #number of seconds for each span of observation
    time_bracket = 3600.0/ConfigHelper.getHourSegments()
    time_end = 0


    while index < len:
        #check if a new bracket needs to be created
        if all_actions[index].time > time_end:
            #update the time


        index += 1

    return csv_data

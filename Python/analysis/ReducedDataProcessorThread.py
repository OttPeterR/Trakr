from database.relational import BehaviorDatabaseHelper
from config import ConfigHelper


# this class will parse through a sorted list of all observations and create a large array of data to be written to output
# puts data into usercount table of behaviorDB

def makeExportData():
    # this is a 2d array of the rows to be exported
    csv_data = []

    conn = BehaviorDatabaseHelper.connect()
    all_actions = BehaviorDatabaseHelper.getAllActionsSortedbyTime(conn)

    index = 0
    leng = len(all_actions)

    # number of seconds for each span of observation
    time_bracket = 3600.0 / ConfigHelper.getHourSegments()
    time_end = -1
    current_entries = 0
    current_exits = 0
    last_population = 0

    for action in all_actions:
        # this is guaranteed to hit on the first packet
        # check if a new bracket needs to be created
        if action.time > time_end:
            # update the time


            # each time stamp will be the start time
            # and the next observation will be when it ends
            csv_data += [(time_end,
                          current_entries,
                          current_exits,
                          last_population)]

            # reset counters
            time_end = action.time + time_bracket
            last_population = last_population + current_entries - current_exits
            current_entries = 0
            current_exits = 0

        # is it an entry?
        if action.action == 1:
            current_entries += 1
        # else, it's an exit:
        else:
            current_exits += 1

        index += 1

    return csv_data

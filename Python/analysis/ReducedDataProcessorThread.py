from database.relational import BehaviorDatabaseHelper
from config import ConfigHelper


# this class will parse through a sorted list of all observations and create a large array of data to be written to output
# puts data into usercount table of behaviorDB

def makeExportData():
    # this is a 2d array of the rows to be exported
    csv_data = []

    conn = BehaviorDatabaseHelper.connect()
    all_actions = BehaviorDatabaseHelper.getAllActionsSortedbyTime(conn)

    # number of seconds for each span of observation
    time_bracket = 3600 / ConfigHelper.getHourSegments()
    time_end = all_actions[0].time
    current_entries = 0
    current_exits = 0
    current_population = 0
    current_addresses = []  # make me a dictionary of (address, time)
    # each time will be an entry time and when called it will be called
    # with the action that is the corresponding exit
    # from there a timespan can be calculated and decided if it should be kept
    # or not, use config: entry_time


    for action in all_actions:
        # this is guaranteed to hit on the first packet
        # check if a new bracket needs to be created
        if action.time > time_end:
            # update

            current_population = current_population + current_entries - current_exits

            # each time stamp will be the start time
            # and the next observation will be when it ends
            csv_data += [(time_end,
                          current_entries,
                          current_exits,
                          current_population)]

            # reset counters
            time_end = time_end + time_bracket
            current_entries = 0
            current_exits = 0

        # entry
        if action.action == 1:
            current_entries += 1
           # current_addresses += [(action.address, action.time)]
        # exit
        else:
            current_exits += 1
#            current_addresses.remove(action.address)

    return csv_data[1:]

from database.relational import BehaviorDatabaseHelper
from database.relational.BehaviorDatabaseHelper import SimpleAction
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

    filtered_actions = all_actions#__filterActions(all_actions)

    for action in filtered_actions:
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

        # exit
        else:
            current_exits += 1
    return csv_data[1:]


def __filterActions(all_actions):
    filtered_actions = []
    entries = []
    for a in all_actions:
        # if its an entry, just log it in the list
        if a.action == 1:
            entries += [EntryAction(a.time, a.address)]
        # if it's an exit, we need to see if we're cutting it out
        else:
            prev = __findEntryTime(a.address, entries)
            timespan = a.time - prev
            # should we keep it?
            if timespan > ConfigHelper.getEntryTime():
                filtered_actions += [SimpleAction(1, a.time, a.address)]
                filtered_actions += [SimpleAction(0, prev, a.address)]

    # now everything in filtered_actions are likely to be non-randomized MAC address devices
    # need to sort by time
    filtered_actions.sort()

    return filtered_actions


def __findEntryTime(address, entries):
    for e in entries:
        if e.address == address:
            return e.time
    return None


class EntryAction:
    time = 0
    address = 0

    def __init__(self, time, address):
        self.time = time
        self.address = address

    def __eq__(self, other):
        return self.address == other.address

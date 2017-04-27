import csv
from config import ConfigHelper
import datetime

# puts contents into the file specified, will create it if need be, overwrite otherwise
file_extention = ".csv"


def export(file_path, contents):
    # appending .csv file
    if not file_path.endswith(file_extention):
        file_path += file_extention

    row_timestamp = "timestamp"
    row_entries = "entries"
    row_exits = "exits"
    row_current_population = "current_population"

    file = open(file_path, 'w')
    field_names = [row_timestamp, row_entries, row_exits, row_current_population]
    writer = csv.DictWriter(file, fieldnames=field_names)

    file.write("Starting time: " + __convert_time_full(contents[0][0]) + "\n")
    file.write("Ending time:   " + __convert_time_full(contents[-1][0]) + " (plus monitoring duration of " + str(
        60 / ConfigHelper.getHourSegments()) + " mins)\n")
    file.write("\n")
    file.write(row_timestamp+", "+row_entries+", "+row_exits+", "+row_current_population+"\n")

    for c in contents:
        time = __convert_time(c[0])
        writer.writerow({row_timestamp: time,
                         row_entries: c[1],
                         row_exits: c[2],
                         row_current_population: c[3]})

    file.close()


def __convert_time(t):
    # %Y-%m-%d  =  year-month-day
    # %H:%M:%S  =  hour:minute:second
    return datetime.datetime.fromtimestamp(t).strftime('%H:%M')


def __convert_time_full(t):
    return datetime.datetime.fromtimestamp(t).strftime('%Y-%m-%d %H:%M:%S')

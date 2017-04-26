import csv
from database.relational import BehaviorDatabaseHelper


# puts contents into the file specified, will create it if need be, overwrite otherwise
def export(file_path, contents):
    # appending .csv file
    if not file_path.endswith(".csv"):
        file_path += ".csv"

    row_timestamp = "timestamp"
    row_entries = "entries"
    row_exits = "exits"
    row_current_population = "current_population"


    file = open(file_path, 'w')
    field_names = [row_timestamp, row_entries, row_exits, row_current_population]
    writer = csv.DictWriter(file, fieldnames=field_names)

    for c in contents:
        writer.writerow({row_timestamp:c[0],
                         row_entries:c[1],
                         row_exits:c[2],
                         row_current_population:c[3]})

    print file_path

    file.close()

    pass

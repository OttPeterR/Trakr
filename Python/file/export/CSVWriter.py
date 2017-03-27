import csv
from database.relational import BehaviorDatabaseHelper


def export(file_path):
    # export a csv file that will follow this structure:
    # time stamp, num users within from now to next time stamp, num new users seen, avg. prev. visits for not new users
    # time stamp will increment starting at oldest and going forward

    # most of this data can be taken directly from the database
    pass

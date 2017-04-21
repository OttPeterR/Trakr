class CSVRow:
    start_time = -1
    end_time = -1
    already_present_devices = 0
    new_devices = 0
    exited_devices = 0

    def __init__(self, time, mac, lat, long):
        self.time = time
        self.mac = mac
        self.lat = lat
        self.long = long


def makeRow(starttime, endtime, alreadypresentdevices, newdevices, exiteddevices):
    return CSVRow(starttime, endtime, alreadypresentdevices, newdevices, exiteddevices)

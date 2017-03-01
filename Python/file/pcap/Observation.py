class Observation:
    time = 0.0
    mac = "00:00:00:00:00:00"
    lat = 0.0
    long = 0.0

    def __init__(self, time, mac, lat, long):
        self.time = time
        self.mac = mac
        self.lat = lat
        self.long = long

def makeObservation(packet):
    return Observation(__getTime(packet),
                       __getTransmissionAddress(packet),
                       __getLat(packet),
                    __getLong(packet))

def __getTransmissionAddress(packet):
    if packet.name == "Ethernet":
        return str(packet.src)
    elif packet.name == "RadioTap dummy":
        try:
            return str(packet.addr2)
        except AttributeError:
            return "error"
    else:
        return "unknown"

#UNIX time in seconds
def __getTime(packet):
    return packet.time

def __getLat(packet):
    return 0.0

def __getLong(packet):
    return 0.0
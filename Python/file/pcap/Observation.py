blank_address = "000000000000"
broadcast_address = "ffffffffffff"
ethernet = "Ethernet"
radiotap_dummy = "RadioTap dummy"
error = "error"
unknown = "unknown"
none = "none"
blank = ""
bad_addresses = [blank, error, none, unknown, broadcast_address, blank_address]


class Observation:
    time = 0.0
    mac = blank_address
    lat = 0.0
    long = 0.0

    def __init__(self, time, mac, lat, long):
        self.time = time
        self.mac = mac
        self.lat = lat
        self.long = long

def makeObservation(packet, lat, long):
    return Observation(__getTime(packet),
                       __getTransmissionAddress(packet),
                       lat, long)

def __getTransmissionAddress(packet):
    address = ""
    if packet.name == ethernet:
        address = packet.src
    elif packet.name == radiotap_dummy:
        try:
            address = packet.addr2
        except AttributeError:
            return error
    else:
        return unknown
    return address

#UNIX time in seconds
def __getTime(packet):
    return packet.time


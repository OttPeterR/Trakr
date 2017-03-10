from config import ConfigHelper
from database import PrivacyUtility

bad_addresses = ["", "error", "none", "ffffffffffff", "000000000000"]
blank_address = "000000000000"
ethernet = "Ethernet"
radiotap_dummy = "RadioTap dummy"
error = "error"
unknown = "unknown"

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
    return __processAddress(address)

#UNIX time in seconds
def __getTime(packet):
    return packet.time



def __processAddress(address):

    # convert to just hex
    newAddress = str(address).replace(':', '').lower()

    # catching the non useful MACs
    if address in bad_addresses:
        # don't care about these addresses, just zero them out
        newAddress = blank_address

    # hash the MACs for privacy
    if ConfigHelper.shouldHash():
        newAddress = PrivacyUtility.getHashString(newAddress)  # getting the hex version of the hash of the value
    return newAddress


import hashlib
from config import ConfigHelper
from file.pcap import Observation

def __hash(obj):
    return hashlib.sha256(str(obj)).hexdigest()

def __getHashString(obj):
    return str(int(str(hash(obj)), 16))


def processAddress(address):
    # convert to just hex
    address = str(address).replace(':', '').lower()

    # hash the MACs for privacy
    if ConfigHelper.shouldHash():
        address = __getHashString(address)  # getting the hex version of the hash of the value
    return address
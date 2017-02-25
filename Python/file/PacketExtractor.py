@staticmethod
def getPacketInfo(packet):
    return [-1, -1, -1]


@staticmethod
def getTransmissionAddress(packet):
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
@staticmethod
def getTime(packet):
    return packet.time
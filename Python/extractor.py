from scapy.all import *


def getMACs(pathToPcap):
    count = 0

    print "Reading file, please wait..."
    # this command can take a long time to run
    packets = rdpcap(pathToPcap)

    print "file read complete.\n"

    broadcast_address = "ff:ff:ff:ff:ff:ff"

    for packet in packets:
        count = count + 1
        print str(count) + " - " + str(packet.name)
        # for ethernet packets
        if packet.name == "Ethernet":
            print "src:         " + str(packet.src)
            print "dst:         " + str(packet.dst)


        # for almost anything else
        elif packet.name == "RadioTap dummy":
            try:
                if packet.addr1 == broadcast_address:
                    print "Broadcast    (to all)"
                else:
                    print "Receiver:    " + str(packet.addr1)
                print "Transmitter: " + str(packet.addr2)
                print "Destination: " + str(packet.addr3)

            except AttributeError:
                print "Could not read packet"

        else:
            print "Unhandled packet type"

        print


def getUniqueMACs(pathToPcap):
    count = 0

    print "Reading file, please wait..."
    # this command can take a long time to run
    packets = rdpcap(pathToPcap)

    print "file read complete.\n"

    dict = {}

    for packet in packets:

        # is this a new mac address?
        if getTransAddress(packet) not in dict:
            dict[getTransAddress(packet)] = count
            count = count + 1

    print dict
    print "unique: " + str(len(dict))
    print "total:  " + str(len(packets))


def getTransAddress(packet):
    if packet.name == "Ethernet":
        return packet.src
    elif packet.name == "RadioTap dummy":
        try:
            return packet.addr2
        except AttributeError:
            return "error"
    else:
        return "unknown"


def test():
    # getMACs("/Users/pott/Desktop/few.pcap")
    getUniqueMACs("/Users/pott/Desktop/hub-50k.pcap")


if __name__ == '__main__':
    test()

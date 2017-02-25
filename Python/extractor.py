from scapy.all import *






def printMACs(packets):
    count = 0
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


def getAllMACs(packets):
    macs = []

    for p in packets:
        macs += [str(getTransAddress(p))]

    return macs


def getUniqueMACs(packets):
    ind = 0
    dict = {}
    address = ""

    for packet in packets:
        address = getTransAddress(packet)
        # is this a new mac address?
        if address not in dict:
            dict[address] = ind
            ind = ind + 1


    print dict
    print "unique: " + str(len(dict))
    print "total:  " + str(len(packets))

    return dict

def occurrences(target, allMACs):
    count = 0
    for mac in allMACs:
        if target == mac:
            count += 1
    return count


def getTransAddress(packet):
    if packet.name == "Ethernet":
        return str(packet.src)
    elif packet.name == "RadioTap dummy":
        try:
            return str(packet.addr2)
        except AttributeError:
            return "error"
    else:
        return "unknown"


def loadFile(pathToFile):
    print "Reading file, please wait..."
    # this command can take a long time to run based on file size
    # ram can get gigantic if your file is big
    # expect about 30x RAM usage based on file size
    packets = rdpcap(pathToFile)
    print "file read complete.\n"
    return packets







def test():

    #load up the file
    packets = loadFile(sys.argv[1])

    #can make a dictionary of the unique packets
    dict = getUniqueMACs(packets)

    #can make a list of all MACs seen
    allMacs = getAllMACs(packets)

    #can count how many times you see an address
    count = occurrences(allMacs[0], allMacs)


    print "target: "+str(allMacs[0])
    print "count:  "+str(count)

if __name__ == '__main__':
    test()
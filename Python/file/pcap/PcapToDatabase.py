#move data from pcap files into the first stage of databases
from scapy.all import rdpcap

import PacketExtractor
from database.relational import RollingDatabaseHelper


def loadPcap(pathToPcap):
    #read the packets into an array
    #this takes a relatively very long time
    packets = rdpcap(pathToPcap)


    dbHelper = RollingDatabaseHelper.ComprehensiveDatabaseHelper()
    info = []
    #loop through packets, extract info, throw into database
    for p in packets:
        info = PacketExtractor.getPacketInfo(p)
        dbHelper.load(info)
#move data from pcap files into the first stage of databases
import demo_Extractor


def loadPcap(pathToPcap):
    packets = demo_Extractor.loadFile(pathToPcap)

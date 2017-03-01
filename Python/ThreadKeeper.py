from time import sleep
from time import strftime

global numThreads
numThreads = 0



def getNumThreads():
    global numThreads
    return numThreads

def getTimeStamp():
    return strftime("%Y-%m-%d-%H:%M:%S")

def wait(seconds):
    sleep(seconds)

def waitForThreads():
    global numThreads
    while numThreads > 0:
        sleep(1)


def incrementThreadCount():
    global numThreads
    numThreads = numThreads + 1
    return


def decrementThreadCount():
    global numThreads
    numThreads = numThreads - 1
    return
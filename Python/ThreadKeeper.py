from time import sleep

global numThreads
numThreads = 0



def getNumThreads():
    global numThreads
    return numThreads


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
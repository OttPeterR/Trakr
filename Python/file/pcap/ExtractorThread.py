from ObservationExtractorHelper import extractToObservations
from ObservationProcessorHelper import processObservations
from management import ThreadKeeper


def extract(filePath, latitude=0, longitude=0, allowDeletion=True):
    ThreadKeeper.incrementThreadCount()

    # make the observations
    observations = extractToObservations(filePath, latitude, longitude, allowDeletion)

    # process them
    processObservations(observations)

    ThreadKeeper.decrementThreadCount()
    return

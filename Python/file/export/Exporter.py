# this controls the export process at a high level

# start thread with ReducedDataProcessor
# put that array into a file via CSVWriter
from analysis import ReducedDataProcessor

def export():
    ReducedDataProcessor.beginExport()


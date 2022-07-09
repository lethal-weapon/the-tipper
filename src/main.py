from src.storage.storage import Storage
from src.analysis.roi_range import ROIRange
from src.contents.tipper import Tipper

if __name__ == '__main__':
    Storage.initialize()
    ROIRange.initialize()
    Tipper.launch()

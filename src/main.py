from src.storage.cache import Cache
from src.storage.storage import Storage
from src.analysis.roi_range import ROIRange
from src.contents.tipper import Tipper
from src.utils.database import Database

if __name__ == '__main__':
    Database.connect()
    Cache.initialize()
    Storage.initialize()
    # ROIRange.initialize()
    Tipper.launch()

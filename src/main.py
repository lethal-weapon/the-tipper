from src.storage.storage import Storage
from src.contents.tipper import Tipper

if __name__ == '__main__':
    Storage.initialize()
    Tipper.launch()

from datetime import datetime
from models import (Base, session, Inventory, engine)
import datetime
import csv
import time






if __name__ == '__main__':
    Base.metadata.create_all(engine)

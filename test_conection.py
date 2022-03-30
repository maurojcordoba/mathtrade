
import os
from database import DataBase

database = DataBase()

print(database.get_version())

database.close()
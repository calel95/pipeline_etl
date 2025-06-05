import os
import csv
import zipfile
import pandas as pd
from utils import Util
import datetime


a = Util()
a.zip_extract("202501_Militares.zip")
#filebytes = zipfile.ZipFile("data/origin/202501_Militares.zip")
#filebytes.extractall(f"data/raw/{datetime.datetime.now().strftime('%Y%m%d_%H_%M_%S')}")

import pandas as pd
from datetime import timedelta, date
import os
import requests as req
### Constants used in the program ### 

git = False
debug = False

docType = "Stemming" # possible entries are Verslag or Stemming
kamerleden_dir = "./files/kamerleden/"
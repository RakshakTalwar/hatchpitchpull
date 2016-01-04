"""
Copyright 2016 (c) Rakshak Talwar

Released under the Apache 2 License
"""

import json, pdb
from hatchpitchpull.hatchpitchpull import F6S, GS, DBHandler

# initialize instances
fs = F6S()
gs = GS()
db_handler = DBHandler()

# pull data from F6S site
f6s_data = fs.grab_data()
# store into the respective table
db_handler.save('F_Application', f6s_data)

# pull data from the Google Spreadsheet
gs_data = gs.grab_data()
# store into the respective table
db_handler.save('H_Application', gs_data)

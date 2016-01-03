"""
Copyright 2016 (c) Rakshak Talwar

Released under the Apache 2 License
"""

import json, pdb
from hatchpitchpull.hatchpitchpull import F6S, GS, DBHandler

f = F6S()

items = f.grab_data()

with open('sampledump.json', 'w') as file:
    json.dump(items['data'], file)

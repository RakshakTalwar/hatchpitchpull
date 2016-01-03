"""
Copyright 2016 (c) Rakshak Talwar

Released under the Apache 2 License
"""

import pdb
import sqlite3 as sql
import requests
import gspread

### gather authentication information ###
auth_file_location = 'auth_info.txt'
auth_ls = []
with open(auth_file_location, 'r') as auth_file:
    auth_ls = [item.strip() for item in auth_file.readlines()]
    auth_file.close()
# define global variables for authentication
EMAIL, EMAIL_PWD, F6S_KEY = auth_ls

def grab_f6s_data():
    pass

def grab_gspread_data():
    pass

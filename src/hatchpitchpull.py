"""
Copyright 2016 (c) Rakshak Talwar

Released under the Apache 2 License
"""

import pdb
import sqlite3 as sql
import requests
import gspread

### gather authentication information ###
auth_file_location = 'src/auth_info.txt'
auth_ls = []
with open(auth_file_location, 'r') as auth_file:
    auth_ls = [item.strip() for item in auth_file.readlines()]
    auth_file.close()
# define global variables for authentication
EMAIL, EMAIL_PWD, F6S_KEY = auth_ls

class F6S():
    """Defines object to pull data from F6S API"""
    def grab_data():
        pass

class GS():
    """Defines object to pull data from gspread API"""
    def grab_data():
        pass

class DBHandler():
    """Defines object which handles saving data into the sqlite db"""

    def __init__(self, db_path='db/HATCHscreening.db'):
        # create connection to sqlite database
        self.connection = sql.connect(db_path)

    def save(self, table_name, doc):
        """Saves a JSON document with fields: [data, fields]
        Where data is a list of JSON objects, and fields is a list of fields which corresponds
        with the field names in the respective table"""
        pass

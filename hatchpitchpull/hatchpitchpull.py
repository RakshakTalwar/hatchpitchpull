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

class F6S():
    """Defines object to pull data from F6S API"""
    def __init__(self):
        self.api_key = F6S_KEY
        self.request_url = 'https://api.f6s.com/hatchpitchsxsw2016/applications'

    def grab_data(self):
        """Pulls all relevant data from F6S REST API. Returns a JSON
        object with fields: data and fields (see save method under DBHandler class)"""

        self.all_data = [] # list stores JSON objects of all companies' data

        page = 1
        while True:
            # pull JSON object
            payload = {'page' : page, 'api_key' : self.api_key}
            r = requests.get(self.request_url, params=payload)
            j = r.json() # create JSON object from response

            # extend all_data with data in this json response if the data exists
            if 'data' in j: # check to see if data is present in most recent request
                self.all_data.extend(j['data'])
                page += 1 # increment page variable to pick up new data on next run
            else: # if no data exists, exit this loop
                break

        


class GS():
    """Defines object to pull data from gspread API"""
    def grab_data(self):
        pass

class DBHandler():
    """Defines object which handles saving data into the sqlite db"""
    def __init__(self, db_path='db/HATCHscreening.db'):
        # create connection to sqlite database to make cursor object
        try:
            self.connection = sql.connect(db_path)
            self.cursor = self.connection.cursor()
        except Exception as e:
            raise e

    def save(self, table_name, doc):
        """Saves a JSON document with fields: [data, fields]
        Where data is a list of JSON objects, and fields is a list of fields which corresponds
        with the field names in the respective table"""
        pass

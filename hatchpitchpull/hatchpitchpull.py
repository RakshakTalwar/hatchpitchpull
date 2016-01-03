"""
Copyright 2016 (c) Rakshak Talwar

Released under the Apache 2 License
"""

import pdb, time
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

        # define the field names for the json responses and sql table, field names correspond 1 to 1
        self.sql_fields = [
            "Started On",
        	"Submitted On",
        	"CompanyTeam",
        	"City",
        	"Country",
        	"Industry Sector",
        	"Contact First Name",
        	"Contact Last Name",
        	"Contact Email",
        	"Contact Phone",
        	"Employees",
        	"Founders and Execs",
        	"InvestorsEquity",
        	"Product Launch",
        	"Grapevine",
        	"Accelerators",
        	"Pitching",
        	"Availability",
        	"Agreement",
        	"AppStatus"
        ]
        self.json_fields = [
            "date_created",
            "date_finalized",
            "name",
            ["location", "city"],
            ["location", "country"],
            ["questions", 0, "field_response", '*'],
            ["questions", 4, "question_response"],
            ["questions", 5, "question_response"],
            ["questions", 6, "question_response"],
            ["questions", 7, "question_response"],
            ["questions", 3, "question_response"],
            ["members", '*', "name"],
            ["questions", 2, "question_response"],
            ["questions", 1, "field_response"],
            ["questions", 8, "question_response"],
            ["questions", 9, "question_response"],
            ["questions", 10, "question_response"],
            ["questions", 11, "field_response", '*'],
            ["questions", 12, "field_response", '*'],
            "status"
        ]

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
                time.sleep(0.02) # wait for a bit before submitting next request
            else: # if no data exists, exit this loop
                break

    def _piece_extractor(self, j_object):
        """Extracts the SQL tables corresponding piece of information from a
        JSON object representing a single company. Returns a JSON object with the field
        names that correspond with the needed field names for the SQL table"""



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

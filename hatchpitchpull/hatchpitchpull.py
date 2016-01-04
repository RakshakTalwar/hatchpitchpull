"""
Copyright 2016 (c) Rakshak Talwar

Released under the Apache 2 License
"""

import json, pdb, re, time
import HTMLParser
import sqlite3 as sql
import requests
import gspread
from oauth2client.client import SignedJwtAssertionCredentials

### global variables ###
hparse = HTMLParser.HTMLParser()

### gather authentication information ###
auth_file_location = 'auth_info.txt'
auth_ls = []
with open(auth_file_location, 'r') as auth_file:
    auth_ls = [item.strip() for item in auth_file.readlines()]
    auth_file.close()
# define global variables for authentication
F6S_KEY = auth_ls[0]

class F6S():
    """Defines object to pull data from F6S API"""
    def __init__(self):
        self.api_key = F6S_KEY
        self.request_url = 'https://api.f6s.com/hatchpitchsxsw2016/applications'

        # define the field names for the json responses and sql table, field names correspond 1 to 1
        self.sql_fields = [
            "StartedOn",
        	"SubmittedOn",
        	"CompanyTeam",
        	"City",
        	"Country",
        	"IndustrySector",
        	"ContactFirstName",
        	"ContactLastName",
        	"ContactEmail",
        	"ContactPhone",
        	"Employees",
        	"FoundersandExecs",
        	"InvestorsEquity",
        	"ProductLaunch",
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
        """Pulls all relevant data from F6S REST API. Returns a dict
         with fields: data and fields (see save method under DBHandler class)"""

        self.all_data = [] # list stores JSON objects of all companies' data

        page = 1
        while page:
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
                page = False

        return {'data' : self._piece_extractor(self.all_data), 'fields' : self.sql_fields}

    def _piece_extractor(self, j_objects):
        """Extracts the SQL tables corresponding piece of information from a
        dict representing a single company. Returns a list of dicts
        where the field names correspond with the needed field names for the SQL table"""

        self.cleaned_objs = [] # a list of cleaned JSON objects to be returned

        # go through each object from the F6S API calls and create semi-copies with relevant and corresponding fields
        for j_object in j_objects:

            # create a temporary object, will be appended to the cleaned_objs list
            temp_obj = {}

            # fill up the temp_obj with the relevant information
            for index, sql_field in enumerate(self.sql_fields):

                # handle the different types of nested data sequences
                if isinstance(self.json_fields[index], str): # if the field is directly present, no nesting
                    temp_obj[sql_field] = j_object[self.json_fields[index]]

                elif isinstance(self.json_fields[index], list): # handles nested cases

                    nest_list = self.json_fields[index] # for brevity's sake

                    if len(nest_list) == 2:
                        temp_obj[sql_field] = j_object[nest_list[0]][nest_list[1]]

                    elif len(nest_list) == 3:
                        # note there are two types of nest_list of length 3, we need to handle them seperately
                        if isinstance(nest_list[1], int): # the first type is where item at index 1 is an integer
                            temp_obj[sql_field] = hparse.unescape(j_object[nest_list[0]][nest_list[1]][nest_list[2]])
                        elif nest_list[1] == '*': # the second type is where item at index 1 is an asterisk (*)
                            # in this case we need to cycle through the list given after we pull it from j_object.
                            # then we join all of the values given in the field from nest_list[2]
                            str_to_return = ''
                            for item in j_object[nest_list[0]]:
                                str_to_return = str_to_return + ', ' + item[nest_list[2]]

                            temp_obj[sql_field] = str_to_return.encode('ascii', 'ignore')

                    elif len(nest_list) == 4:
                        str_to_return = ''
                        if isinstance(j_object[nest_list[0]][nest_list[1]][nest_list[2]], list):
                            for item in j_object[nest_list[0]][nest_list[1]][nest_list[2]]:
                                str_to_return = item + ', ' + str_to_return
                        elif isinstance(j_object[nest_list[0]][nest_list[1]][nest_list[2]], str):
                                str_to_return = j_object[nest_list[0]][nest_list[1]][nest_list[2]].encode('ascii', 'ignore')
                        temp_obj[sql_field] = str_to_return

            # add the cleaned object
            self.cleaned_objs.append(temp_obj)

        return self.cleaned_objs

class GS():
    """Defines object to pull data from gspread API"""
    def __init__(self):
        # initialize the client which will communicate with the Google Spreadsheet
        json_key = json.load(open('client_secret.json'))
        scope = ['https://spreadsheets.google.com/feeds']
        credentials = SignedJwtAssertionCredentials(json_key['client_email'], json_key['private_key'], scope)
        self.client = gspread.authorize(credentials)

        # define the field names for the sql table
        self.sql_fields = [
            "SubmittedOn",
            "Company",
            "ShortDescription",
            "City",
            "StateProvince",
            "Country",
            "IndustrySector",
            "CompanyWebsite",
            "CompanySocial",
            "ContactFirstName",
            "ContactLastName",
            "ContactEmail",
            "ContactPhone",
            "Employees",
            "FoundersandExecs",
            "Revenue",
            "CurrentInvestment",
            "Investors",
            "Funding",
            "Launch",
            "Grapevine",
            "Accelerators",
            "Pitching",
            "Availability",
            "Agreement"
        ]

    def grab_data(self, spreadsheet_key='1TgYK4D209oPrmv18-XVodH40JjvU69Xhkfjau3DlQxg', worksheet_name='Sheet1'):
        # open the respective worksheet within the Google Spreadsheet

        self.spreadsheet = self.client.open_by_key(spreadsheet_key)
        self.worksheet = self.spreadsheet.worksheet(worksheet_name)

        # grab all data present within the worksheet, not including headers
        all_data = self.worksheet.get_all_values()[1:]

        return {'data' : all_data, 'fields' : self.sql_fields}


class DBHandler():
    """Defines object which handles saving data into the sqlite db"""
    def __init__(self, db_path='db/HATCHscreening.db'):
        # create connection to sqlite database to make cursor object
        self.db_path = db_path
        self.connection = sql.connect(self.db_path)
        self.cursor = self.connection.cursor()

    def save(self, table_name, doc):
        """Saves a dict with fields: [data, fields]
        Where data is a list of dicts, and fields is a list of fields which corresponds
        with the field names in the respective table"""

        try:
            # create a new connection to sqlite database to make cursor object
            self.connection = sql.connect(self.db_path)
            self.cursor = self.connection.cursor()

            if table_name == 'F_Application':
                self.cursor.executescript("""
                    DROP TABLE IF EXISTS {0};
                    CREATE TABLE {0}(StartedOn DateTime,
                	SubmittedOn DateTime,
                	CompanyTeam TEXT,
                	City TEXT,
                	Country TEXT,
                	IndustrySector TEXT,
                	ContactFirstName TEXT,
                	ContactLastName TEXT,
                	ContactEmail TEXT,
                	ContactPhone TEXT,
                	Employees INTEGER,
                	FoundersandExecs TEXT,
                	InvestorsEquity TEXT,
                	ProductLaunch TEXT,
                	Grapevine TEXT,
                	Accelerators TEXT,
                	Pitching TEXT,
                	Availability TEXT,
                	Agreement TEXT,
                	AppStatus TEXT);
                """.format(table_name))

                self._complete_all_insertions(table_name, doc)

            elif table_name == 'H_Application':
                self.cursor.executescript("""
                    DROP TABLE IF EXISTS {0};
                    CREATE TABLE {0}(SubmittedOn DateTime,
                	Company Text,
                	ShortDescription Text,
                	City Text,
                	StateProvince Text,
                	Country Text,
                	IndustrySector Text,
                	CompanyWebsite Text,
                	CompanySocial Text,
                	ContactFirstName Text,
                	ContactLastName Text,
                	ContactEmail Text,
                	ContactPhone Text,
                	Employees INTEGER DEFAULT 0,
                	FoundersandExecs Text,
                	Revenue REAL,
                	CurrentInvestment REAL DEFAULT 0,
                	Investors Text,
                	Funding Text,
                	Launch DateTime,
                	Grapevine Text,
                	Accelerators Text,
                	Pitching Text,
                	Availability Text,
                	Agreement Text);
                """.format(table_name))

                self._complete_all_insertions(table_name, doc)

            self.connection.commit()

        except Exception as e:
            if self.connection:
                self.connection.rollback()
            raise e
        finally:
            if self.connection:
                self.connection.close()

    def _complete_all_insertions(self, table_name, doc):
        """Returns a list with all insertion commands to be used
        Accepts the data returned by grab_data method"""

        # fill the insertion_string with contents
        for item in doc['data']:
            vals = []
            if table_name == 'F_Application':
                for key in doc['fields']:
                    vals.append(item[key])
            elif table_name == 'H_Application':
                vals.extend(item)
            placeholders = "({0})".format(len(vals) * '?, ') # generate SQL friendly placeholders string
            placeholders = placeholders[:-3] + ')' # remove the trailing comma
            sql_command = "INSERT INTO {0} VALUES {1}".format(table_name, placeholders)
            self.cursor.execute(sql_command, vals) # interpolate values into SQL command

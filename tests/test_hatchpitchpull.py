"""
Copyright 2016 (c) Rakshak Talwar

Released under the Apache 2 License
"""

from hatchpitchpull.hatchpitchpull import F6S, GS, DBHandler

### Testing F6S class ###
def test_grab_data():
    pass

### Testing GS class ###
def test_grab_data():
    pass

### Testing DBHandler class ###
def test_init():
    inst = DBHandler(db_path='db/HATCHscreening.db')
# create a new instance to test the other methods below
inst = DBHandler(db_path='db/HATCHscreening.db')
def test_save():
    pass
def test_existing_names():
    assert isinstance(inst._existing_names('H_Application'), list)

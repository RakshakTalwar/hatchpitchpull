"""
Copyright 2016 (c) Rakshak Talwar

Released under the Apache 2 License
"""

from hatchpitchpull.hatchpitchpull import F6S, GS, DBHandler

### Testing F6S class ###
def test_init():
    f_inst = F6S()
# create a new instance to test the other methods below
f_inst = F6S()
def test_grab_data():
    assert f_inst.grab_data()

### Testing GS class ###
def test_init():
    g_inst = GS()
# create a new instance to test the other methods below
g_inst = GS()
def test_grab_data():
    assert g_inst.grab_data()

### Testing DBHandler class ###
def test_init():
    d_inst = DBHandler(db_path='db/HATCHscreening.db')
# create a new instance to test the other methods below
d_inst = DBHandler(db_path='db/HATCHscreening.db')
def test_save():
    pass

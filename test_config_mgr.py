"""
# tests for patch_ini_file.py
# the function should not change or care what the current working directory is.
# the function can be used to compare 2 files for equality or similarity
"""

VALID_INI_FILE = 'sample.ini' # sample data file
VALID_INI_FILE_JSON = 'sample.dict'
MISSING1 = 'notThere.ini'
MISSING2 = 'Gone.ini'
TEST1 = 'temp_test1.ini'
TEST2 = 'temp_test2.ini'

from config_mgr import patch_ini_file
from config_mgr import parse_ini_file_into_dict
# define tests for patch_ini_file()

import json
import pytest

# the function should not change or care what the current working directory is.
# the function can be used to compare 2 files for equality or similarity
# the function should throw exceptions if either file is missing.
# test missing files
def test_missing_both_files():
    with pytest.raises(IOError):
        patch_ini_file(MISSING1, MISSING2)

def test_missing_second_file():
    with pytest.raises(IOError):
        patch_ini_file(VALID_INI_FILE, MISSING1)

def test_missing_first_file():
    with pytest.raises(IOError):
        patch_ini_file(MISSING2, VALID_INI_FILE)

# now create a dummy default file (using existing issabove.conf file for now)
def test_proper_function_with_matching_files():
    from shutil import copyfile
    copyfile(VALID_INI_FILE, TEST1)
    # create a custom file that matches default file
    copyfile(TEST1, TEST2)
    # test function against files, verify files still equal
    patch_ini_file(TEST1, TEST2)
    assert patch_ini_file(TEST1, TEST2, PATCH=False, EXACT=False) == True
    assert patch_ini_file(TEST1, TEST2, PATCH=False, EXACT=True) == True
        #exact allows for FUZZY test such as file2 is a superset of file1

# create custom file missing a section and some value
def test_that_files_are_different():
    from random import choice
    from ConfigParser import SafeConfigParser
    customINI = SafeConfigParser()
    customINI.read(TEST2)
    sections = customINI.sections()
    customINI.remove_section(choice(sections))
    with open(TEST2, "wb") as config_file:
        customINI.write(config_file)
    assert patch_ini_file(TEST1, TEST2, PATCH=False, EXACT=False) == False
    assert patch_ini_file(TEST1, TEST2, PATCH=False, EXACT=True) == False

# test function against files, verify that custom file has been updated
def test_proper_function_with_differing_files():
    assert patch_ini_file(TEST1, TEST2, PATCH=False, EXACT=False) == False
    assert patch_ini_file(TEST1, TEST2, PATCH=False, EXACT=True) == False
    patch_ini_file(TEST1, TEST2)
    assert patch_ini_file(TEST1, TEST2, PATCH=False, EXACT=False) == True
    assert patch_ini_file(TEST1, TEST2, PATCH=False, EXACT=True) == False

# add an extra section to customfile and verify that it still passes a file comparison (supersets of default allowed)
def test_proper_function_when_custom_is_superset_of_default():
    from ConfigParser import SafeConfigParser
    customINI = SafeConfigParser()
    customINI.read(TEST2)
    customINI.add_section('NewDummySection')
    with open(TEST2, "wb") as config_file:
        customINI.write(config_file)
    assert patch_ini_file(TEST1, TEST2, PATCH=False, EXACT=False) == True
    assert patch_ini_file(TEST1, TEST2, PATCH=False, EXACT=True) == False

# parse ini file into a dictionary
def test_can_parse_ini_file_into_dict():
    # recover json file containing dict version of sample INI file.
    with open(VALID_INI_FILE_JSON) as data_file:    
        ini_dict = json.load(data_file)

    assert parse_ini_file_into_dict(VALID_INI_FILE) == ini_dict


# teardown temporary files
#TODO delete test1
#TODO delete test2

# report success
#not needed since pytest communicates status
# tests for patch_ini_file.py
# the function should not change or care what the current working directory is.
# the function can be used to compare 2 files for equality or similarity

valid_ini_file = 'sample.ini' # sample data file
missing1 = 'notThere.ini'
missing2 = 'Gone.ini'
test1 = 'temp_test1.ini'
test2 = 'temp_test2.ini'

from config_mgr import patch_ini_file
# define tests for patch_ini_file()

import pytest

# the function should not change or care what the current working directory is.
# the function can be used to compare 2 files for equality or similarity
# the function should throw exceptions if either file is missing.
# test missing files
def test_missing_both_files():
    with pytest.raises(IOError):
        patch_ini_file(missing1, missing2)

def test_missing_second_file():
    with pytest.raises(IOError):
        patch_ini_file(valid_ini_file, missing1)

def test_missing_first_file():
    with pytest.raises(IOError):
        patch_ini_file(missing2, valid_ini_file)

# now create a dummy default file (using existing issabove.conf file for now)
def test_proper_function_with_matching_files():
    from shutil import copyfile
    copyfile(valid_ini_file, test1)
    # create a custom file that matches default file
    copyfile(test1, test2)
    # test function against files, verify files still equal
    patch_ini_file(test1, test2)
    assert patch_ini_file(test1, test2, PATCH=False, EXACT=False) == True
    assert patch_ini_file(test1, test2, PATCH=False, EXACT=True) == True #exact allows for FUZZY test such as file2 is a superset of file1

# create custom file missing a section and some value
def test_that_files_are_different():
    from random import choice
    from ConfigParser import SafeConfigParser
    customINI = SafeConfigParser()
    customINI.read(test2)
    sections = customINI.sections()
    customINI.remove_section(choice(sections))
    with open(test2, "wb") as config_file:
        customINI.write(config_file)
    assert patch_ini_file(test1, test2, PATCH=False, EXACT=False) == False
    assert patch_ini_file(test1, test2, PATCH=False, EXACT=True) == False

# test function against files, verify that custom file has been updated
def test_proper_function_with_differing_files():
    assert patch_ini_file(test1, test2, PATCH=False, EXACT=False) == False
    assert patch_ini_file(test1, test2, PATCH=False, EXACT=True) == False
    patch_ini_file(test1, test2)
    assert patch_ini_file(test1, test2, PATCH=False, EXACT=False) == True
    assert patch_ini_file(test1, test2, PATCH=False, EXACT=True) == False

# add an extra section to customfile and verify that it still passes a file comparison (supersets of default allowed)
def test_proper_function_when_custom_is_superset_of_default():
    from ConfigParser import SafeConfigParser
    customINI = SafeConfigParser()
    customINI.read(test2)
    customINI.add_section('NewDummySection')
    with open(test2, "wb") as config_file:
        customINI.write(config_file)
    assert patch_ini_file(test1, test2, PATCH=False, EXACT=False) == True
    assert patch_ini_file(test1, test2, PATCH=False, EXACT=True) == False

# teardown temporary files

# report success
"""
    scan the sample INI files for parsing errors
"""
import os

from config_mgr import ini_file_can_be_parsed

CWD = os.getcwd()
CWD = CWD + '/test/sample_ini_files/'

FILELIST = os.listdir(CWD)

for filename in FILELIST:
    print filename
    ini_file_can_be_parsed(CWD + filename)

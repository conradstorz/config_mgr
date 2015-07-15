import os

from patch_ini_file import ini_file_can_be_parsed

cwd = os.getcwd()
cwd = cwd + '/test/sample_ini_files/'

filelist = os.listdir(cwd)

for filename in filelist:
    print filename
    ini_file_can_be_parsed(cwd + filename)
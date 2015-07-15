"""
    config_mgr exports 2 functions for managing INI style configuration files.
"""

from ConfigParser import SafeConfigParser
from filecmp import cmp as filecompare

def patch_ini_file(defaultfile, customfile, PATCH=True, EXACT=False):
    """
        Compare 2 .INI format files and ensure that at minimum customfile contains ALL sections and options from defaultfile.
        If PATCH is True and EXACT is False update customfile without changing any custom option values.
        If EXACT is True and PATCH is True erase all custom values and duplicate default entirely.
        IF PATCH is False then only compare files and return True if files match.
        EXACT determines if files need to be identical to match.
    """
    default_options = SafeConfigParser()
    result = default_options.read(defaultfile) # returns an empty list if file error
    if result == []:
        raise IOError

    personalized_options = SafeConfigParser()
    result = personalized_options.read(customfile)
    if result == []:
        raise IOError

    personalized_options_have_been_modified = False
    personalized_and_default_are_same = True

    #iterate through default file and compare customfile for existance of each field
    for section_name in default_options.sections():
        if personalized_options.has_section(section_name) == False:
            personalized_options.add_section(section_name) #create section name in customfile
            personalized_options_have_been_modified = True
            personalized_and_default_are_same = False
        for option_name in default_options.options(section_name):
            defaultvalue = default_options.get(section_name, option_name)
            if personalized_options.has_option(section_name, option_name) == False:
                personalized_options.set(section_name, option_name, defaultvalue) #create name/value pair in customfile
                personalized_options_have_been_modified = True
                personalized_and_default_are_same = False
            else:
                if personalized_options.get(section_name, option_name) != defaultvalue:
                    personalized_and_default_are_same = False #keep track of dissimilarities in files

    # local(in memory) copy of customfile now contains all sections and options of defaultfile.
    if personalized_options_have_been_modified and PATCH:
        with open(customfile, "wb") as config_file:
            if EXACT: #with PATCH and EXACT we discard the old customfile and replace with defaultfile
                default_options.write(config_file)
            else: #otherwise with PATCH only we write the patched version of customfile to storage
                personalized_options.write(config_file)

    #for purposes of comparison of files regardless of patching return True/False
    if EXACT:
        return filecompare(defaultfile, customfile)
    else:
        return personalized_and_default_are_same

def ini_file_can_be_parsed(filename):
    """
        use patch_ini_file function to test a file for correctness as an INI file
    """
    from ConfigParser import ParsingError as ParseError
    from ConfigParser import InterpolationSyntaxError as InterpError
    import sys
    result = False
    print
    print 'testing: ' + filename
    try:
        result = patch_ini_file(filename, filename)
        print "good."
    except ParseError:
        print "File contains parsing error(s)", sys.exc_info()[0], sys.exc_info()[1]
    except InterpError:
        print "File contains interpolation error(s)", sys.exc_info()[0], sys.exc_info()[1]
    return result

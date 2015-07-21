# README #

This question that I have copied from Stack Overflow clearly states (and expands upon) my motivation for this project.
I have made some changes to the original discussion.
You can find it at:
http://stackoverflow.com/questions/6133517/parse-config-file-environment-and-command-line-arguments-to-get-a-single-coll?answertab=active#tab-top
-------------------------------------------
Python's standard library has modules for configuration file parsing (configparser), environment variable reading (os.environ), and command-line argument parsing (argparse). I want to write a program that does all those, and also:

    Has a cascade of option values:
1        default option values, overridden by
2        config file options, overridden by
3        environment variables, overridden by
4        command-line options and finally
5        placing everything into a python data structure
         for the host program to access.

        ADDITIONALLY;
        The host program may modify these option values
        and then ask that they be saved to the config file
        from item 2 above.

    Allows a configuration file location specified on the command line with e.g. --config-file foo.conf, and reads that instead of the usual configuration file. This must still obey the above cascade.

    Allows option definitions in a single place to determine the parsing behaviour for configuration files and the command line. (EDIT I don't know what the author intended by this. -Conrad Storz)

Everything I need is apparently in the Python standard library, but they don't work together smoothly.

How can I achieve this with minimum deviation from the Python standard library?
-------------------------------------------
As of 7-16-2015 my project has the ability to manage steps 1 and 2 outlined above using a pair of files formated in a INI style layout.

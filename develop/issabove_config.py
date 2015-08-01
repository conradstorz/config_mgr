#    import pdb; pdb.set_trace()
"""
    This is an implementation of config_mgr written by Conrad Storz to specifically meet the needs of the fine program
    written by Liam Kennedy called ISS-ABOVE. config_mgr is used here to read a file of configuration options and place
    the results into a data structure used by the ISS-ABOVE program.
"""
from config_mgr import patch_ini_file
from config_mgr import parse_ini_file_into_dict


def load_ISSABOVE_config(configFile, options):
    """
        get custom settings from ISS-ABOVE configuration file
    """
    ISSABOVE_defaults = 'issabove.conf.default.txt'

    patch_ini_file(ISSABOVE_defaults, config_file) #compare custom to default and add any missing default items to custom
    
    #now read all custom items into a python dictionary
    options_dict = parse_ini_file_into_dict(config_file)

    def get_item(section, item):
        import string
        value = ''
        if section in options_dict:
            if item in options_dict[section]:
                value = options_dict[section][item]
            else:
                print 'Missing configuration item: "{}" in section: "{}"'.format(item, section)
        else:
            print 'Missing configuration section: "{}"'.format(section)

        #check string for boolean value
        if value == 'True':
            return True
        if value == 'False':
            return False

        #check string for integer or float value
        parseStr = lambda x: x.isalpha() and x or x.isdigit() and \
                                int(x) or x.isalnum() and x or \
                                len(set(string.punctuation).intersection(x)) == 1 and \
                                x.count('.') == 1 and float(x) or x
        return parseStr(value)

            
    #place the custom options into the variables used by ISS-ABOVE
    obs_location = get_item('Location', 'city'), get_item('Location', 'lat'), get_item('Location', 'lon')
    op.elevation = int( get_item('Location', 'elevation') )
    op.city = obs_location[0]
    op.lat = obs_location[1]
    op.lon = obs_location[2]

    op.daysToRefresh = get_item('options', 'daystorefresh')
    op.stationName = get_item('options', 'stationname')
    print 'Station Name: ', op.stationName
    op.locationName = get_item('options', 'locationname')
    print 'Location name ' + op.locationName
    op.minAlt = get_item('options', 'minalt')
    print 'Minimum Altitude to process: ', op.minAlt
    op.metric = get_item('options', 'metric')

    op.postLocation = get_item('ISSAboveToWordpress', 'postlocation')
    op.post = get_item('ISSAboveToWordpress', 'post')
    op.tweetAlt = get_item('ISSAboveToWordpress', 'tweetalt')
    print 'Auto Tweet if Alt reaches: ', op.tweetAlt
    op.publish = get_item('ISSAboveToWordpress', 'publish')
    print "Read Publish:", op.publish
    op.username = get_item('ISSAboveToWordpress', 'username')
    op.password = get_item('ISSAboveToWordpress', 'password')
    op.postContent = get_item('ISSAboveToWordpress', 'postcontent')

    op.tweetMessages = options_dict['TWEETmessages'].keys()
    op.tweet1 = get_item('TWEETmessages', 'tweet1')
    op.tweet2 = get_item('TWEETmessages', 'tweet2')
    op.tweet3 = get_item('TWEETmessages', 'tweet3')
    op.tweet4 = get_item('TWEETmessages', 'tweet4')

    op.displayDevices = options_dict['DisplayDevices'].keys()
    print 'display Devices: ', op.displayDevices

    for display in op.displayDevices :
        if display == 'piglow' :
            op.piglow = True
            print 'piglow'
        if display =='pilite' :
            op.pilite = True
            print 'pilite'
        if display == 'ledborg' :
            op.ledborg = True
            print 'ledborg'
        if display == 'lcdrgb' :
            op.lcdrgb = True
            print 'LCD - RGB version'
        if display == 'lcdsinglecolor' :
            op.lcdsinglecolor=True
            print 'LCD - Single Color version'
        if display == 'blinkstick' :
            op.blinkstick = True
            print 'BlinkStick'
        if display =='isslight' :
            op.isslight = True
        if display == 'blink1' :
            op.blink1 = True
            print 'blink(1) from ThingM'
        if display == 'pifacecad':
            op.pifacecad = True
            print 'PiFace Control & Display'
  
    op.imageurl = get_item('www', 'imageurl')
    op.imagewidth = get_item('www', 'imagewidth')
    op.imageheight = get_item('www', 'imageheight')
    print "imageurl =",op.imageurl
    op.wwwport = get_item('www', 'port')

    op.timezone = get_item('Location', 'timezone')

    op.adminusername = get_item('options', 'adminusername') 
    op.adminpassword = get_item('options', 'adminpassword') 
    op.adminpasswordrequired = get_item('options', 'adminpasswordrequired')

    op.wpurl = get_item('ISSAboveToWordpress', 'wpurl')
    print "WP posting reconfigured to : ", op.wpurl

    op.celestrakTLE = get_item('TLEconfig', 'celestrak')
    op.NASATLE = get_item('TLEconfig', 'NASA')

    op.NASAtweet = get_item('options', 'NASAtweet')

    op.TLEpref = get_item('TLEconfig', 'TLEpref')

    op.FirstTimeSetup = get_item('Setup', 'firsttimesetup')
    op.ShutdownOnFirstBoot = get_item('Setup', 'shutdownonfirstboot')

    op.hdvideoenabled = get_item('hdvideo', 'hdvideoenabled')
    op.hdvideochannel = get_item('hdvideo', 'hdvideochannel')
    op.hdvideostream = get_item('hdvideo', 'hdvideostream')
    op.hdevalwayson = get_item('hdvideo', 'hdevalwayson')
    op.hdevon = get_item('hdvideo', 'hdevon')
    print 'hdev On time: ', op.hdevon
    op.hdevoff = get_item('hdvideo', 'hdevoff')
    print 'hdev Off time: ', op.hdevoff

    op.crewID = get_item('crew', 'id')
    print 'crew ID: ', op.crewID

    op.versionurl = get_item('version', 'updateurl')
    op.autoupdate = get_item('version', 'autoupdate')
    return True


import ConfigParser
config_tle = 'issabove.tle'
config_file = 'issabove.conf'
class issaboveOptions:
      def __init__(self):
          self.locationName = 'Undefined Location'
          self.stationName = 'Undefined station'
          self.timezone = 'America/Los Angeles'
          self.elevation = 0 #height above sea level in meters
          self.lat= '34.1477'
          self.lon= '-118.1436'
          self.minAlt = 0.0 #the LED lights won't activate unless the pass is higher than this.
          self.donotdisturb = False #This will eventually allow the LED lights to "go quiet" at night - so it won't light up and wake up the cats/dogs/children/mice
          self.dndstart = "23:30"     #not working in this version
          self.dndend = "06:00"
          self.metric = True
          self.location = 'Pasadena, CA', 34.1477, -118.1436
          self.daysToRefresh = 5
          self.postLocation = True
          self.post = True
          self.tweetAlt = 30
          self.publish = True
          self.username = 'issabove-default'
          self.password = ''
          self.postContent = """This message was created by an ISS-Above that is in Pasadena, CA<br /><br /> 
             This little device lights up whenever The International Space Station is overhead.  <br /><br />
             You can make one too"""
          self.tweetMessages = [ ['tweet1', 'Hello to the ISS and everyone up there!'], \
                             ['tweet2', 'I hope everyone in the ISS is having a GREAT day!'], \
                             ['tweet3', "How's it hanging in the ISS today?"] ]
          self.piglow = False 
          self.pilite = False
          self.ledborg = False
          self.lcdrgb = False
          self.lcdsinglecolor = False
          self.blinkstick = False
          self.pifacecad = False
          self.blink1 = False
          self.isslight = False
          self.GPIOearth = 25 #gpio pin to flash something attached to GPIO pin 25
          self.GPIOiss = 23 #gpio pin to flash something attached to GPIO pin 24
          self.pitft = False # Yes... working on this
          self.displayDevices = []
          self.imageurl = 'http://issabove.com/wp-content/uploads/2013/12/ISS-Above-Logo-sm.png'
          self.imageheight = "194"
          self.imagewidth = "300"
          self.wwwport="80"
          self.adminusername = "admin"
          self.adminpassword = "nasa"
          self.superuser = "issabove" #just in case someone forgets their password and are not Raspberry Pi experts..  I have implemented a special password that will allow access to the admin functions.  
          self.disablesuperuser = False #and this can be disabled by adding a disablesuperuser = True line in the "options" section of /home/pi/issabove/issabove.conf file.  
          self.adminpasswordrequired = True #if [options] adminpasswordrequired is set to False then admin functions do not require any password.  
                                       # Not recommended for a publicly accessible ISS-Above (for a public setup you should do other things to harden your device).
          
          self.wpurl = "http://issabove.com/xmlrpc.php" # it is possible to configure the ISS-Above to post to any server... just change this url... 
                                                        # or add a value for wpurl to the issabove.conf file [to the ISSAboveToWordpress] section
                                                        # e.g. [ISSAboveToWordpress]
                                                        #      wpurl = mysite.com/xmlrpc.php
                                                        # Changing this is NOT supported (i.e. don't call me.. if you know enough to do this.. you should be able to handle everything about this change) 
          
          # [options]
          # NASAtweet = "@NASA_Johnson"
          self.NASAtweet = "@Space_Station"  
          self.NASAtweet2 = "@NASA_Johnson" 
          
          # optional in conf file.
          # [TLEconfig]
          # celestrakTLE = "blah.com/blah.txt"
          # NASATLE = "nasa.gov/blah.html" 
          # tlepref = celestrak # celestrak or NASA
            
          self.celestrakTLE = "http://www.celestrak.com/NORAD/elements/stations.txt"  
          self.NASATLE = "http://spaceflight.nasa.gov/realdata/sightings/SSapplications/Post/JavaSSOP/orbit/ISS/SVPOST.html"
          self.TLEpref = "celestrak" # "celestrak" or "NASA"  
          
          self.FirstTimeSetup = False # don't run the web based First Setup feature 
                                      # This feature pulls in the setup information for the Kickstarter backer.
          self.ShutdownOnFirstBoot = False #After first setup - the next boot will auto-shut-down

          ####################################
          ## ISS HD Live Experiment Settings
          ####################################

          self.hdvideoenabled = False
          self.hdvideochannel = "http://www.ustream.tv/channel/iss-hdev-payload"
          self.hdvideostream = "best"
          self.hdevalwayson = False
          self.hdevon = 10
          self.hdevoff = 5
                    
          #self.channels = []
          #self.channels.append( ['http://www.ustream.tv/channel/iss-hdev-payload', ['480p_alt_akamai','720p+','240p_alt_akamai']] )
          #self.defaultChannel = ( 0,0 )
          #self.
          
          self.overlayfontscale = 1.2
          
          #New settings for the autoupdate system.
          self.versionurl = "http://issabove.com/wp-content/uploads/2015/06/code_version.txt"
          self.autoupdate = False 
          self.crewID = 44.0
op = issaboveOptions()


def loadconfig() :
    global iss_tle, obs_location, debugpanel, config_file, op, config_tle, iss_tle_date, options, currentTZ
    
    # this is the TLE data
    config = ConfigParser.ConfigParser()
    config.read(config_tle)

    """
    # this is the main issoptions file.  
    options = ConfigParser.ConfigParser(allow_no_value=True)
    options.read( config_file )
    """  
    load_ISSABOVE_config(config_file, op)

    """ this section is not being tested at this time     
    try :             
        iss_tle = config.get('TLE', 'line1',0), config.get('TLE', 'line2',0), config.get('TLE', 'line3',0)
    except :
           print "Error loading TLE data from " 
           logging.warning( 'Error loading TLE data from file.  recreating '+config_file )      
           writedefaultconfig()
           config.read(config_tle)
           iss_tle = config.get('TLE', 'line1',0), config.get('TLE', 'line2',0), config.get('TLE', 'line3',0)

    try :
        iss_tle_date = datetime.strptime(config.get( 'TLE', 'date', 0), '%b %d %Y')
        print "TLE date: ", iss_tle_date
    except :
           print "old TLE data"
           logging.warning('The ISS TLE data is the default and could be very old')
           iss_tle_date = datetime.now() + timedelta(days=-30)  
    # check to see if the TLE data is out of date.  
    checkTLEoutofdate()

    
    try :
        currentTZ = getRPiTimezone() 
    except :
           currentTZ = 'Unknown (this is a bug...odd)'
           pass
           
    if op.timezone <> currentTZ :
        print "TIMEZONE ISSUE: Config file says we should be in : " + op.timezone + " but this device is configured for " + currentTZ
        print "*"+op.timezone+"*"
        print "*"+currentTZ+"*"

    """

    #override video stream only if it's configured for the main hdev video channel.       
    if op.hdvideochannel == "http://www.ustream.tv/channel/iss-hdev-payload" :      
        op.hdvideostream = "mobile_478p"
        print "Stream Override:", op.hdvideostream
    return True          


if __name__ == '__main__':
    loadconfig()

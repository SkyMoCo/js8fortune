# we are using the major.minor.patch notation
# patch number increase indicates a bug fix
# minor number increase means the addition of a feature but remaining backward compatible with earlier releases
# major number increase indicates a significant change to the code that means it is no longer backward compatible
__version__ = "0.01.0"

# make sure port 2442 is open on your firewall for access from 127.0.0.1 prior to opening JS8 application
# ubuntu command: sudo ufw allow 2442
# in JS8Call go to File -> Settings -> Reporting in API section check:
# Enable TCP Server API
# Accept TCP Requests

server = ('127.0.0.1', 2442)
msg_terminator = '♢'

announce = True
mb_announcement_timer = 60  # in minutes, suggested values are 60, 30 and 15

# Location of the fortunes files
# the posts_dir value must be enclosed in quotes and end with \\ or /
# the posts_dir value (and hence directory path) can contain spaces
fortunes_dir = '/var/tmp/fortunes/'
replace_nl = False  # if True, \n characters in a post will be replaced with a space character

# when debugging this code, JS8Call must be running but a radio isn't needed
debug = False  # set to True to tests with simulated messages set in debug_json

#######################################################################################################

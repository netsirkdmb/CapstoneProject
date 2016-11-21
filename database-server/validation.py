###############################################################################################
# Kristen Dhuse, Bryant Hall, William McCumstie                                               #
# CS419 - API                                                                                 #
# Description: This validates input for the employee recognition system API.                  #
# References:                                                                                 #
# - for help email validation using regex                                                     #
#       http://emailregex.com/                                                                #
# - for help with datetime validation                                                         #
#       http://stackoverflow.com/questions/18539266/how-to-validate-a-specific-date-and-time-format-using-python
# - for help with datetime formatting                                                         #
#       http://strftime.org/                                                                  #
###############################################################################################


import re
from datetime import datetime

def emailValidation(string):
    pattern = re.compile("(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
    return pattern.match(string)

def datetimeValidation(string):
    try:
        datetime.strptime(string, "%Y-%m-%d %H:%M:%S")
        return True
    except ValueError:
        return False
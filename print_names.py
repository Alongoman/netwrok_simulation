import datetime

CYELLOW = '\033[33m'
CBPURPLE = '\033[45m'
CEND = '\033[0m'

# Run this script before you take screenshots

# TODO: fill your names & ID numbers

name_ID_1 = "Alon Goldmann 312592173"
name_ID_2 = "Peleg Goldberger 206173585"
date_time = datetime.datetime.now()

print (CBPURPLE + name_ID_1 + " | " + name_ID_2 + " | " + date_time.strftime("%c") + CEND)
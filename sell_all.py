import time


from api import *
from keys import *
from trade import *

############################################################################################
#  Main Loop
############################################################################################

# basic API check 
markets = call_api(method='/public/getmarkets')
if not markets['success']:
    print("Api doesn't work")
    SystemExit()
    
sell_all()
print("DONE")

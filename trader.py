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

start = True

while True:
    try:
        # check current orders, if order is not executed in ORDER_LIFE_TIME, adjust price
        if adjust_open_orders(not start):
            time.sleep(1)
        else:
            time.sleep(5)
            
        start = False

    except Exception as e:
        print(e)


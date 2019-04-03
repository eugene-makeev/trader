import time


from api import *
from keys import *
from logger import *
from trade import *


############################################################################################
#  Main Loop
############################################################################################

# print all available markets
markets = call_api(method='/public/getmarkets')
if markets['success']:
    print(markets['result'])
else:
    print("Api doesn't work")
    SystemExit()

start = True

while True:
    try:
        # 0. cancel all open orders since they are most likely not actual anymore
        # 1. check current orders, if order is not executed in ORDER_LIFE_TIME, adjust price
        open_orders = adjust_open_orders(not start)

        start = False
        if open_orders == True:
            time.sleep(1)
        else:
            time.sleep(5)

    except Exception as e:
        print(e)


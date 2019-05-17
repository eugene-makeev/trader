import time


from api import *
from keys import *
from trade import *


to_buy = {
          'BCH': 9,
          'ADA': 7000,
          'TRX': 8000,
          'RDD': 133823,
          'XRP': 1000,
         }


############################################################################################
#  Main Loop
############################################################################################

# basic API check 
markets = call_api(method='/public/getmarkets')
if not markets['success']:
    print("Api doesn't work")
    SystemExit()
    
buy_all(to_buy)
print('DONE')
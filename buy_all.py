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

markets_supported = []


def buy_all():
    print('''
    ///////////////////////////////////////////////////////////////////////////////////
    //                                BUY ALL
    ///////////////////////////////////////////////////////////////////////////////////
    ''')
    cancel_orders('SELL')
    
    markets = call_api(method='/public/getmarkets')
    if markets['success']:
        for market in markets['result']:
            pair =  market['BaseCurrency'] + '-' + market['MarketCurrency']
            markets_supported.append(pair)
            
    for (currency, quantity) in to_buy.items():
        pair = 'BTC-' + currency.upper()
        if pair in markets_supported:
            create_buy(pair, quantity)
 
    bougth_in = False
    
    while not bougth_in:
        open_orders = adjust_open_orders()
        
        if not open_orders:
            bougth_in = True
        time.sleep(5)


############################################################################################
#  Main Loop
############################################################################################

# basic API check 
markets = call_api(method='/public/getmarkets')
if not markets['success']:
    print("Api doesn't work")
    SystemExit()
    
buy_all()
print('DONE')
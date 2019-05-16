import time


from api import *
from keys import *
from trade import *

markets_supported = []


def sell_all(sell_btc=False):
    print('''
    ///////////////////////////////////////////////////////////////////////////////////
    //                                SELL ALL
    ///////////////////////////////////////////////////////////////////////////////////
    ''')
    cancel_orders('BUY')
    
    markets = call_api(method='/public/getmarkets')
    if markets['success']:
        for market in markets['result']:
            pair = market['MarketCurrency'] + '-' +  market['BaseCurrency']
            markets_supported.append(pair)

    balances = call_api(method='/account/getbalances')
    if balances['success']:
        for balance in balances['result']:
            if balance['Available']:
                if balance['Currency'] == 'BTC':
                    if sell_btc:
                        create_sell('USDT-BTC', balance['Available'])
                elif balance['Currency'] != 'USDT':
                    market = 'USDT-' + balance['Currency']
                    if market not in markets_supported:
                        market = 'BTC-' + balance['Currency']
                    create_sell(market, balance['Available'])

    sold_out = False
    
    while not sold_out:
        if sell_btc:
            balance = call_api(method='/account/getbalance', currency='USDT-BTC')
            if balance['result']:
                btc_available = float(balance['result']['Available'])
                if btc_available:
                    create_sell('USDT-BTC', btc_available)
        open_orders = adjust_open_orders()
        
        if not open_orders:
            sold_out = True
        time.sleep(5)


############################################################################################
#  Main Loop
############################################################################################

# basic API check 
markets = call_api(method='/public/getmarkets')
if not markets['success']:
    print("Api doesn't work")
    SystemExit()
    
sell_all()

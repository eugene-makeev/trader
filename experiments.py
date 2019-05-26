import time
from api import *

btc_markets = {}
usdt_markets = {}
eth_markets = {}
usd_markets = {}

def get_markets():
# basic API check 
    markets = call_api(method='/public/getmarkets')
    if markets['success']:
        for market in markets['result']:
            #print(market)
            if market['IsActive'] and market['IsRestricted'] == False:
                if market['BaseCurrency'] == 'BTC':
                    btc_markets[market['MarketName']] = market['MinTradeSize']
                elif market['BaseCurrency'] == 'USDT':
                    usdt_markets[market['MarketName']] = market['MinTradeSize']
                elif market['BaseCurrency'] == 'ETH':
                    eth_markets[market['MarketName']] = market['MinTradeSize']
                elif market['BaseCurrency'] == 'USD':
                    usd_markets[market['MarketName']] = market['MinTradeSize']
        return True
    return False
 
def get_market_summary(market):
    market_summary = call_api(method='/public/getmarketsummary', market=market)
    if market_summary['success']:
        return market_summary['result']

    return None

 
if get_markets():
    print('BTC markets:', len(btc_markets), btc_markets)
    print('USDT markets:', len(usdt_markets), usdt_markets)
    print('ETH markets:', len(eth_markets), eth_markets)
    print('USD markets:', len(usd_markets), usd_markets)



#market_summaries = call_api(method='/public/getmarketsummaries')
#if market_summaries['success']:
#    for summary in sorted(market_summaries['result'], reverse=True, key=lambda k: (k['BaseVolume'])):
#        if summary['BaseVolume'] >= 1.0:
#            print (summary)


############################################################################################
#  Main Loop
############################################################################################
            



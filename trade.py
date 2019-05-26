from api import *
from timeframe import *
from colors import *

markets_supported = []

def cancel_orders(orders_type='ALL'):
    print('''
    ///////////////////////////////////////////////////////////////////////////////////
    //                            CANCEL %s ORDERS
    ///////////////////////////////////////////////////////////////////////////////////
    ''' % orders_type)
    orders = call_api(method='/market/getopenorders')
    if orders['success']:
        for order in orders['result']:
            order_type = order["OrderType"].split('_')[-1]
            if orders_type == 'ALL' or order_type == orders_type:
                print("\t* cancel %s order for %s" % (order_type, order['Exchange']))
                cancel_res = call_api(method="/market/cancel", uuid=order['OrderUuid'])
                print("\t\tsuccess:", cancel_res['success'], cancel_res['message'])
    else:
        print("failed to get open orders:", orders['message'])

def is_rate_changed(order):
    order_type = order["OrderType"].lower().split('_')[-1]
    # check competitor order validity
    order_book = call_api(method="/public/getorderbook", market=order['Exchange'], type=order_type)
    if order_book['success']:
        for competitor in order_book['result']:
            if competitor['Rate'] * DEBUG_PRICE_RATE != order['Limit']:
                # TODO: ckeck if MIN_COMPETITOR_ORDER_VOLUME is suitable for altcoins
                if competitor['Quantity'] >= MIN_COMPETITOR_ORDER_VOLUME:
                    return True
            else:
                return False
    else:
        print('failed to get order book data')
        
    return False

def adjust_open_orders(create_new=True):
    open_orders = 0
    print('''
    ///////////////////////////////////////////////////////////////////////////////////
    //                            ADJUST OPEN ORDERS
    ///////////////////////////////////////////////////////////////////////////////////
    ''')
    orders = call_api(method='/market/getopenorders')
    if orders['success']:
        open_orders = len(orders['result'])
        print('\tOpen orders:', open_orders)
        for order in orders['result']:
            opened = get_time_from_str(order['Opened'])
            print('\t%s %s, quantity: %0.8f, created: %s' % (order["OrderType"], order['Exchange'],
                                                             order['QuantityRemaining'], opened))
            if is_rate_changed(order):
                order_type = order["OrderType"].split('_')[-1]
                if cancel_order(order['OrderUuid'], order_type) and create_new:
                    quantity = order['QuantityRemaining']
                    if order_type == 'SELL':
                        create_sell(order['Exchange'], quantity)
                    else:
                        create_buy(order['Exchange'], quantity)
    else:
        print(CRED, "failed to get open orders:", orders['message'], CEND)
        
    return open_orders

def get_markets_supported():
    if not len(markets_supported):
        markets = call_api(method='/public/getmarkets')
        if markets['success']:
            for market in markets['result']:
                pair = market['BaseCurrency'] + '-' + market['MarketCurrency']
                markets_supported.append(pair)
    
def sell_all(sell_btc=False):
    print('''
    ///////////////////////////////////////////////////////////////////////////////////
    //                                SELL ALL
    ///////////////////////////////////////////////////////////////////////////////////
    ''')
    cancel_orders('BUY')
 
    get_markets_supported()

    balances = call_api(method='/account/getbalances')
    if balances['success']:
        for balance in balances['result']:
            if balance['Available']:
                if balance['Currency'] == 'BTC':
                    if sell_btc:
                        create_sell('USDT-BTC', balance['Available'])
                elif balance['Currency'] != 'USDT':
                    if sell_btc:
                        market = 'USDT-' + balance['Currency']
                    #if market not in markets_supported:
                    else:
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


def buy_all(pairs=None):
    print('''
    ///////////////////////////////////////////////////////////////////////////////////
    //                                BUY ALL
    ///////////////////////////////////////////////////////////////////////////////////
    ''')
    cancel_orders('SELL')
    
    get_markets_supported()

    if pairs == None:
        print("buy_all Empty pairs not imlemented")
    else:
        for (currency, quantity) in pairs.items():
            pair = 'BTC-' + currency.upper()
            if pair in markets_supported:
                create_buy(pair, quantity)
 
    bougth_in = False
    
    while not bougth_in:
        open_orders = adjust_open_orders()
        
        if not open_orders:
            bougth_in = True
        time.sleep(5)
        
        
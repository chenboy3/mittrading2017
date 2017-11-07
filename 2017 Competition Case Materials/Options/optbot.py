import tradersbot as tt
import time
import mibian
import math

t = tt.TradersBot(host='127.0.0.1', id='trader0', password='trader0')
SPREAD = 0.05
spot = 100
puts = {}
calls = {}
vols = {}
put_greeks = {}
call_greeks = {}
start = time.time()

order_id = []
info = []

history = {} # ticker : [isBuy, quantity, price]

def f(msg, order):
    global spot
    print msg
    for k in msg:
        print k
    state =  msg['market_state']
    for s in state:
        print s
    ticker = state['ticker']
    direction = ticker[-1]
    val = ticker[1:-1]
    if 'ask_price' in msg['market_state'] and 'bid_price' in msg['market_state']:
        price = (max(msg['market_state']['bids'], key=int) + min(msg['market_state']['asks'], key=int)) / 2
    else:
        price = msg['market_state']['last_price']
    #this is a put
    if direction == 'P':
        puts[val] = price
    elif direction == 'C':
        calls[val] = price
    elif ticker == 'TMXFUT':
        spot = price
        print 'TIIIICK', ticker
    else:
        print 'WEEEEEEIRD'

    # do we still want to keep all the old puts/calls?
    print puts, calls
    print 'SPOOOT', spot
    vals()

    smileTrade(order)
    #cancelOrders(order)

    if 'ask_price' in msg['market_state'] and 'bid_price' in msg['market_state']:
        price = (max(msg['market_state']['bids'], key=int) + min(msg['market_state']['asks'], key=int)) / 2

        mid = (max(msg['market_state']['bids'], key=int) + min(msg['market_state']['asks'], key=int)) / 2
        if abs(mid - min(msg['market_state']['asks'], key=int)) * 1.0 / mid >= SPREAD:
            #makeMarket(ticker, val, direction, mid, order)

def vals():
    time_left = 450 - (time.time() - start)
    prev = None
    for call in calls:
        val = mibian.BS([spot, call, 0, time_left/15.0], callPrice = calls[call], volatility = prev)
        vols[call] = val.impliedVolatility
        # not sure if this is the correct way to calculate implied volatility
        prev = val.impliedVolatility
        print vols[call]
        # greeks
        call_greeks[call] = (val.impliedVolatility, val.callDelta, val.vega, val.gamma)
    prev = None
    for put in puts:
        val = mibian.BS([spot, put, 0, time_left/15.0], putPrice = puts[put], volatility = prev )
        vols[put] = val.impliedVolatility
        prev = val.impliedVolatility
        print vols[put]
        put_greeks[put] = (val.impliedVolatility, val.putDelta, val.vega, val.gamma)

def makeMarket(ticker, val, direction, mid, order):
    if direction == 'P':
        delta = put_greeks[val][0]
    else:
        delta = call_greeks[val][0]
    if delta > 0:
        # make a put offer if delta favors calls
        makeTrade(ticker[:-1] + 'P', True, 5, int(mid * 0.95), order)
    else:
        makeTrade(ticker[:-1] + 'C', True, 5, int(mid * 1.05), order)

def cancelOrders(order):
        global order_id
        global info
        print('cancellling')
        print(len(order_id))
        if (len(order_id) == 0):
                print('zeo')
                return
        for i in range(len(order_id)):
                print('can')
                order.addCancel(info[i], order_id[i])
                print('done')
        order_id = []
        info = []

def h(msg, order):
        if 'orders' in msg:
                for k in msg['orders']:
                        order_id.append(k['order_id'])
                        info.append(k['ticker'])


def smileTrade(order):
    #global put_greeks
    global call_greeks
    global spot
    index = 80
    difference = 1000
    ll = []
    for k in call_greeks:
        ll.append(k)
    ll = sorted(ll)
    for i in range(len(ll)):
        diff = abs(spot - call_greeks[ll[i]][0])
        if diff < difference:
                index = i
                difference = diff
    print('eeeereirjeijriejrieji')
    print call_greeks
    print 'doodoooododoo'
    for i in range(index, len(ll) - 1):
        #if the volatility
        print call_greeks[ll[i]][0]
        if ( call_greeks[ll[i+1]][0] < call_greeks[ll[i]][0]):
            ticker = "T"+str(i+1)+"C"
            makeTrade(ticker, True, 1000, calls[ll[i+1]]*1.05, order)
    for i in range(index, 1):
        #if the volatility
        print call_greeks[ll[i]][0]
        if ( call_greeks[ll[i-1]][0] < call_greeks[ll[i]][0]):
            ticker = "T"+str(i-1)+"C"
            makeTrade(ticker, True, 1000, calls[ll[i-1]]*1.05, order)
    print 'dooooon'
    for i in range(len(ll)):
        print ll[i]


def makeTrade(ticker, isBuy, quantity, price, order):
        if ticker not in history:
                history[ticker] = []
        history[ticker].append([isBuy, quantity, price])
        order.addTrade(ticker, isBuy, quantity, price)


t.onMarketUpdate = f
#t.onTrade = g
t.onAckModifyOrders = h
#t.onTraderUpdate = i
t.run()

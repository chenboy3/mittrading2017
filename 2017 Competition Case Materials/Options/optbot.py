import tradersbot as tt
import time
import mibian
import math

t = tt.TradersBot(host='127.0.0.1', id='trader0', password='trader0')
SPREAD = 0.05
spot = 100
#TRADE_LIMIT = 20
puts = {}
calls = {}
vols = {}
put_greeks = {}
call_greeks = {}
start = time.time()

threshold = 0


order_id = []
info = []

history = {} # ticker : [isBuy, quantity, price]

def f(msg, order):
    print 'f'
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
    print('frown')
    #cancelOrders(order)

    if 'ask_price' in msg['market_state'] and 'bid_price' in msg['market_state']:
        price = (max(msg['market_state']['bids'], key=int) + min(msg['market_state']['asks'], key=int)) / 2

        mid = (max(msg['market_state']['bids'], key=int) + min(msg['market_state']['asks'], key=int)) / 2
        #if abs(mid - min(msg['market_state']['asks'], key=int)) * 1.0 / mid >= SPREAD:
            #makeMarket(ticker, val, direction, mid, order)

    print 'frownnnn'

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
    print 'h'
    global threshold
    if 'orders' in msg:
            for k in msg['orders']:
                    order_id.append(k['order_id'])
                    info.append(k['ticker'])
                    threshold -= 1

def i(msg, order):
    print 'i'
    status = msg['trader_state']['positions']
    delta, vega = calcNetDeltaVega(status)
    for ticker in calls:
        if call_greeks[ticker][1] != None and call_greeks[ticker][1] <= abs(delta):
            if delta > 0:
                makeTrade('T' + ticker + 'C', False, abs(delta/call_greeks[ticker][1]), 1.05 * calls[ticker], order)
            else:
               makeTrade('T' + ticker + 'C', True, abs(delta/call_greeks[ticker][1]), 1.05 * calls[ticker], order)
            break

    '''
    get net delta and vega from our positions

    hedge delta and vega

    find stocks to buy/sell such that delta/vega approach 0

    delta of 100, stock has delta of 1

    try to just do delta


    '''

def calcNetDeltaVega(positions):
    net_delta = 0
    net_vega = 0
    # print(positions)
    # print(put_greeks)
    # print(call_greeks)
    for ticker in positions:
        if ticker[-1] == 'P' and ticker[1:-1] in put_greeks and put_greeks[ticker[1:-1]][1] != None:
            net_delta += put_greeks[ticker[1:-1]][1]
            net_vega += put_greeks[ticker[1:-1]][2]
        elif ticker[-1] == 'C' and ticker[1:-1] in call_greeks and call_greeks[ticker[1:-1]][1] != None:
            print call_greeks[ticker[1:-1]]
            net_delta += call_greeks[ticker[1:-1]][1]
            net_vega += call_greeks[ticker[1:-1]][2]
    return net_delta, net_vega

def smileTrade(order):
    index = 1000
    difference = 1000
    call_ll = sorted(list(call_greeks))
    put_ll = sorted(list(put_greeks))
    for i in range(len(call_ll)):
        diff = abs(spot - call_greeks[call_ll[i]][0])
        if diff < difference:
                index = i
                difference = diff
    print('eeeereirjeijriejrieji')
    print call_greeks
    print 'doodoooododoo'
    if index == 1000:
        return
    mean = call_greeks[call_ll[index]][0]
    for i in range(index, len(call_ll) - 1):
        print i
        mean = mean * 0.2 + 0.8 * call_greeks[call_ll[i]][0]
        #if the volatility
        print call_greeks[call_ll[i]][0]
        if ( call_greeks[call_ll[i+1]][0] < mean ):
            ticker = "T"+str(call_ll[i+1])+"C"
            print('iiiiiiiiiin')
            print ticker
            print (calls[call_ll[i+1]]*1.05)
            price = round(calls[call_ll[i+1]]*1.05, 2)
            makeTrade(ticker, True, 1, price, order)

    index = 1000
    difference = 1000
    if index == 1000:
        return
    print put_ll
    for i in range(len(put_ll)):
        print put_greeks[put_ll[i]]
        diff = abs(spot - put_greeks[put_ll[i]][0])
        if diff < difference:
                index = i
                difference = diff
    mean = put_greeks[put_ll[index]][0]
    for i in range(min(len(put_ll) - 1, index), 1, -1):
        print i
        mean = mean * 0.2 + 0.8 * put_greeks[put_ll[i]][0]
        #if the volatility
        print put_greeks[put_ll[i]][0]
        if ( put_greeks[put_ll[i-1]][0] > mean):
            ticker = "T"+str(put_ll[i-1])+"P"
            print('pppppiiiiiiiiiin')
            print ticker
            print (puts[put_ll[i-1]]*0.95)
            price = round(puts[put_ll[i-1]]*1.05,2)
            makeTrade(ticker, True, 1, price, order)
                    #puts[put_ll[i-1]]*0.95, order)
    print 'dooooon'


def makeTrade(ticker, isBuy, quantity, price, order):
#    global threshold
#    if threshold < TRADE_LIMIT:
    if ticker not in history:
            history[ticker] = []
    history[ticker].append([isBuy, quantity, price])
    order.addTrade(ticker, isBuy, quantity, price)
#        threshold += 1

t.onMarketUpdate = f
#t.onTrade = g
#t.onAckModifyOrders = h
#t.onTraderUpdate = i
t.run()

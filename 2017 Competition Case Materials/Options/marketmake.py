import tradersbot as tt
import time
import mibian
import math

t = tt.TradersBot(host='127.0.0.1', id='trader0', password='trader0')
call = {}
put = {}
spot = (100.0, 100.0)
history = {}
last = 0.0
order_id = []
info = []
pdelta = {}
cdelta = {} 
delta = 0.0
def f(msg, order):
    global last
    state =  msg['market_state']
    ticker = state['ticker']
    direction = ticker[-1]
    val = ticker[1:-1]
    if len(state['bids'])==0 or len(state['asks'])==0:
        return
    bid = float((max(msg['market_state']['bids'], key=float)))
    ask = float((min(msg['market_state']['asks'], key=float)))
    if direction == 'P':
        put[val] = (bid, ask)
    elif direction == 'C':
        call[val] = (bid, ask)
    elif ticker == 'TMXFUT':
        spot = (bid, ask)
        print 'TIIIICK', ticker
    else:
        print 'WEEEEEEIRD'
    if (time.time() - last) > 1: 
        last = time.time()
        cancelOrders(order)
        for c in call:
            b = call[c][0]
            a = call[c][1]
            m = (b + a) / 2
            tick = "T"+str(c)+"C"
            if (a - b) / m > 0.05:
                makeTrade(tick, True, 5, b + 0.01, order)
                makeTrade(tick, False, 5, a - 0.01, order)
def vals():
    time_left = 450 - (time.time() - start)
    total_volatility, vol_count = 0, 0
    sspot = spot[0] + spot[1] / 2
    for cal in call:
        val = mibian.BS([sspot, cal, 0, time_left/15.0], callPrice = call[cal][0] + call[cal][1] / 2)
        cdelta[call] = val.delta

    for pu in put:
        val = mibian.BS([sspot, pu, 0, time_left/15.0], putPrice = put[pu][0] + put[pu][1] / 2)
        pdelta[pu] = val.delta

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
'''
'''
def h(msg, order):
    print 'h'
    #global threshold
    if 'orders' in msg:
            for k in msg['orders']:
                    order_id.append(k['order_id'])
                    info.append(k['ticker'])
    #                threshold -= 1
'''
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
'''

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

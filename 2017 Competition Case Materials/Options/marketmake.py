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
start = time.time()
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
        #print 'TIIIICK', ticker
    if (time.time() - last) > 1:
        last = time.time()
        cancelOrders(order)
        # for c in call:
        #     b = call[c][0]
        #     a = call[c][1]
        #     m = (b + a) / 2
        #     tick = "T"+str(c)+"C"
        #     if (a - b) / m > 0.05:
        #         if delta < 10:
        #             makeTrade(tick, True, 5, b + 0.01, order)
        #         if delta > -10:
        #             makeTrade(tick, False, 5, a - 0.01, order)

        # 22
        if delta > -10 and delta < 10:
            # 11 - calls
            for tup in getWidestMarkets(11, False, True):
                #print('TUP')
                #print(tup)
                b = call[tup[0][1:-1]][0]
                a = call[tup[0][1:-1]][1]
                m = (b + a) / 2
                tick = tup[0]
                if (a - b) / m > 0.05:
                    makeTrade(tick, True, 5, b + 0.01, order, time.time())
                    makeTrade(tick, False, 5, a - 0.01, order, time.time())
        else:
            # 2, figure out direction
            for tup in getWidestMarkets(22, False, True):
                b = call[tup[0][1:-1]][0]
                a = call[tup[0][1:-1]][1]
                m = (b + a) / 2
                tick = tup[0]
                if (a - b) / m > 0.05:
                    if delta < 10:
                        makeTrade(tick, True, 5, b + 0.01, order, time.time())
                    if delta > -10:
                        makeTrade(tick, False, 5, a - 0.01, order, time.time())
        if delta > -10 and delta < 10:
            # 11 - calls
            for tup in getWidestMarkets(11, True, False):
                #print('TUP')
                #print(tup)
                b = put[tup[0][1:-1]][0]
                a = put[tup[0][1:-1]][1]
                m = (b + a) / 2
                tick = tup[0]
                if (a - b) / m > 0.05:
                    makeTrade(tick, True, 5, b + 0.01, order, time.time())
                    makeTrade(tick, False, 5, a - 0.01, order, time.time())
        else:
            # 2, figure out direction
            for tup in getWidestMarkets(22, True, False):
                b = put[tup[0][1:-1]][0]
                a = put[tup[0][1:-1]][1]
                m = (b + a) / 2
                tick = tup[0]
                if (a - b) / m > 0.05:
                    if delta > 10:
                        makeTrade(tick, True, 5, b + 0.01, order, time.time())
                    if delta < -10:
                        makeTrade(tick, False, 5, a - 0.01, order, time.time())


def getWidestMarkets(amt, puts, calls):
    ls = []
    if calls:
        for ticker in call:
            tup = call[ticker]
            mid = (tup[0] + tup[1])/2
            ls.append(('T' + ticker + 'C', (tup[1] - mid) * 1.0 / mid))
    if puts:
        for ticker in put:
            tup = put[ticker]
            mid = (tup[0] + tup[1])/2
            ls.append(('T' + ticker + 'P', (tup[1] - mid) * 1.0 / mid))
    ls = sorted(ls, key = lambda tup: tup[1])[::-1]
    if len(ls) < amt:
        return ls
    return ls[:amt]

def vals():
    time_left = 450 - (time.time() - start)
    total_volatility, vol_count = 0, 0
    sspot = spot[0] + spot[1] / 2
    for cal in call:
        #print time_left
        val = mibian.BS([sspot, cal, 0, time_left/15.0], callPrice = (call[cal][0] + call[cal][1]) / 2)
        #print "--------dasfs----"
        #print val.callDelta
        #print val.impliedVolatility
        #print sspot
        #print cal
        #print time_left/15.0
        #print (call[cal][0] + call[cal][1]) / 2

        #cdelta[call] = val.callDelta

    for pu in put:
        val = mibian.BS([sspot, pu, 0, time_left/15.0], putPrice = put[pu][0] + put[pu][1] / 2)
        #pdelta[pu] = val.putDelta

def cancelOrders(order):
        global order_id
        global info
        #print('cancellling')
        #print(len(order_id))
        if (len(order_id) == 0):
                print('zeo')
                return
        for i in range(len(order_id)):
                #print('can')
                order.addCancel(info[i], order_id[i])
                #print('done')
        order_id = []
        info = []
def h(msg, order):
    #print 'h'
    #global threshold
    if 'orders' in msg:
            for k in msg['orders']:
                    order_id.append(k['order_id'])
                    info.append(k['ticker'])
    #                threshold -= 1
def i(msg, order):
    global delta
    delta = 0
    #print 'i'
    status = msg['trader_state']['positions']
    #print status
    #vals()
    for key in status:
        #print key[-1]
        #print delta
        if key[-1] == "P":
            #print key[1:-1]
            #a = 0
            #if key[1:-1] in pdelta:
            #    a = pdelta.get(key[1:-1])
            a = -1
            delta += a * float(status[key])
        else:
            a = 1
            #print key[1:-1]
            #a = 0
            #if key[1:-1] in pdelta:
            #    a = cdelta.get(key[1:-1])
            delta += a * float(status[key])
            #delta += (cdelta.get([key[1:-1],0.0))*float(status[key])
    #print 'DELELLLTA'
    #print delta

lasty = 0
count = 0
def makeTrade(ticker, isBuy, quantity, price, order, time):
    global lasty
    global count
    if ticker not in history:
            history[ticker] = []
    history[ticker].append([isBuy, quantity, price])
    if time > lasty + 1:
        print("TRADES MADE THIS SECOND")
        print(count)
        count = 0
        lasty = time
    else:
        count += 1
    order.addTrade(ticker, isBuy, quantity, price)

t.onMarketUpdate = f
#t.onTrade = g
t.onAckModifyOrders = h
t.onTraderUpdate = i
t.run()

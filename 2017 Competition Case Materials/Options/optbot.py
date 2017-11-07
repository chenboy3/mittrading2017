import tradersbot as tt
import time
import mibian

t = tt.TradersBot(host='127.0.0.1', id='trader0', password='trader0')

spot = 100
puts = {}
calls = {}
vols = {}
put_greeks = {}
call_greeks = {}
start = time.time()

order_id = []
info = []


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

    cancelOrders(order)

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
        call_greeks[call] = (val.callDelta, val.vega, val.gamma)
    prev = None
    for put in puts:
        val = mibian.BS([spot, put, 0, time_left/15.0], putPrice = puts[put], volatility = prev )
        vols[put] = val.impliedVolatility
        prev = val.impliedVolatility
        print vols[put]
        put_greeks[put] = (val.putDelta, val.vega, val.gamma)

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
                        #print('iiddd')
                        #print(k['order_id'])
                        info.append(k['ticker'])

t.onMarketUpdate = f
#t.onTrade = g
t.onAckModifyOrders = h
#t.onTraderUpdate = i
t.run()

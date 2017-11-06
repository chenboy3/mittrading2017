import tradersbot as tt
import time
import mibian

t = tt.TradersBot(host='127.0.0.1', id='trader0', password='trader0')

spot = 100
puts = {}
calls = {}
vols = {}
start = time.time()


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
    print puts, calls
    print 'SPOOOT', spot
    vals()

def vals():
    time_left = 450 - (time.time() - start)
    for call in calls:
        val = mibian.BS([spot, call, 0, time_left/15.0], callPrice = calls[call])
        vols[call] = val.impliedVolatility
        print vols[call]





t.onMarketUpdate = f
#t.onTrade = g
#t.onAckModifyOrders = h
#t.onTraderUpdate = i
t.run()
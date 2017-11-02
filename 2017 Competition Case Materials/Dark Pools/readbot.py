import tradersbot as tt
import time

t = tt.TradersBot(host='127.0.0.1', id='trader0', password='trader0')

vals = ['EUR', 'USD', 'CHF', 'JPY', 'CAD']
pub = ['USDCAD', 'EURUSD', 'USDCHF', 'USDJPY']
dark = ['EURCAD', 'EURJPY', 'EURCHF', 'CHFJPY']
prices = {}

history = {} # ticker : [isBuy, quantity, price]
portfolio = {'USD': 100000.0, 'EUR': 0.0, 'CHF': 0.0, 'JPY': 0.0, 'CAD': 0.0}

trade_ids = set()
order_id = []
info = []
last_trade = 0.0
last = time.time()



for v in vals:
        prices[v] = {}
        for vv in vals:
                prices[v][vv] = 0.0



def f(msg, order):
        global last_trade
        # get the market data and update
        ticker = msg['market_state']['ticker']
        # use last as price for now, can use something more sophisticated
# like weighted mid later
        price = msg['market_state']['last_price']
        update(ticker, price)
        #printVals()
        #cancelOrders(order)
        #for id in order_id:
        #       print(id)
        #if ticker == 'EURCAD':
        #makeTrade('EURUSD', True, 100, price, order)
        #makeTrade('EURCAD', True, 100, price, order)
        for d in dark:
                updateDark(d, prices, order)
        elapsed = time.time() - last
        print elapsed
        if (time.time() - last_trade > 1 and elapsed < 5):
                print('trade')
                last_trade = time.time()
                cancelOrders(order)
                for d in dark:
                        price = prices[d[0:3]][d[3:6]]
                        if price > 0.01:
                                print('buyz' ,d, price * .995)
                                print('sellz',d, price * 1.005)
                                #makeTrade(d, True, 10, price * .999 - .01 + 199, order)
                                makeTrade(d, True, 10, price * .95 - .01, order)
                                makeTrade(d, False, 10, price * 1.05 + .01, order)
        if elapsed > 5:
            print("LIQUIDATING")
            liquidateToUsd(order)
            print("post liquidation")
        '''print('portfolio')
        for p in portfolio:
                print (p)
                print (portfolio[p])'''

def g(msg, order):
    for trade in msg['trades']:
        print('YOOOO')
        print(trade)

        if trade['buy_order_id'] in trade_ids or trade['sell_order_id'] in trade_ids:
            print('INNN')
            first_ticker = trade['ticker'][0:3]
            sec_ticker = trade['ticker'][3:6]
            quantity = trade['quantity']
            price = trade['price']
            isBuy = trade['buy']
            if trade['buy_order_id'] in trade_ids:
                portfolio[first_ticker] += quantity
                portfolio[sec_ticker] -= quantity * price
            else:
                portfolio[first_ticker] -= quantity * price
                portfolio[sec_ticker] += quantity

    print ('hey')
    print msg
def updateDark(ticker, prices, order):
        #print('hee')
        a = ticker[0:3]
        b = ticker[3:6]
        for c in pub:
                for d in pub:
                        c1 = c[0:3]
                        c2 = c[3:6]
                        d1 = d[0:3]
                        d2 = d[3:6]
                        #print(c1, d2)
                        if c1 == d2:
                                #print('a')
                                #print(c2, b)
                                if c2 == b:
                                        #print('b')
                                        if d1 == a:
                                                #print('c')
                                                price = prices[c1][c2] * prices[d1][d2]
                                                prices[a][b] = price
                                                prices[b][a] = price
                                                print ('yoticker: ',ticker,' price: ',price)
                                                '''if price > 0:
                                                        print('yo')
                                                        print(ticker, price * .99)
                                                        if (time.time() - last)
                                                        makeTrade(ticker, True, 100, price * .99, order)
                                                        makeTrade(ticker, False, 100, price * 1.01, order)'''



def printVals():
        print('---------')
        for v in vals:
                for vv in vals:
                        print(v, vv, prices[v][vv])


def update(ticker, price):
        if (len(ticker) != 6):
                return
        a = ticker[0:3]
        b = ticker[3:6]
        prices[a][b] = price
        prices[b][a] = price
        print ('ticker: ',ticker,' price: ',price)


def makeTrade(ticker, isBuy, quantity, price, order):
        if ticker not in history:
                history[ticker] = []
        history[ticker].append([isBuy, quantity, price])
        order.addTrade(ticker, isBuy, quantity, price)


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

def liquidateToUsd(order):
        print('STAAAART')
        print(portfolio)
        # not working, maybe if something's negative
        if portfolio['EUR'] != 0.0:
            if portfolio['EUR'] < 0.0:
                makeTrade('EURUSD', True, int(portfolio['EUR'] * 1.0 / prices['EUR']['USD']), prices['EUR']['USD'], order)
            else:
                makeTrade('EURUSD', False, int(portfolio['EUR'] * 1.0 / prices['EUR']['USD']), prices['EUR']['USD'], order)
        return
        if portfolio['CAD'] != 0.0:
            if portfolio['CAD'] < 0.0:
                makeTrade('USDCAD', True, portfolio['CAD'] * 1.0 / prices['USD']['CAD'], prices['USD']['CAD'], order)
            else:
                makeTrade('USDCAD', False, portfolio['CAD'] * 1.0 / prices['USD']['CAD'], prices['USD']['CAD'], order)
        if portfolio['CHF'] != 0.0:
            if portfolio['CHF'] < 0.0:
                makeTrade('USDCHF', True, portfolio['CHF'] * 1.0 / prices['USD']['CHF'], prices['USD']['CHF'], order)
            else:
                makeTrade('USDCHF', False, portfolio['CHF'] * 1.0 / prices['USD']['CHF'], prices['USD']['CHF'], order)
        if portfolio['JPY'] != 0.0:
            if portfolio['JPY'] < 0.0:
                makeTrade('USDJPY', True, portfolio['JPY'] * 1.0 / prices['USD']['JPY'], prices['USD']['JPY'], order)
            else:
                makeTrade('USDJPY', False, portfolio['JPY'] * 1.0 / prices['USD']['JPY'], prices['USD']['JPY'], order)
        print('EEEENDDD')
def h(msg, order):
        #print('heeeey')
        #print(msg['orders'])
        #for id in order_id:
        #       print(id)
        if 'orders' in msg:
                for k in msg['orders']:
                        trade_ids.add(k['order_id'])
                        order_id.append(k['order_id'])
                        #print('iiddd')
                        #print(k['order_id'])
                        info.append(k['ticker'])


t.onMarketUpdate = f
t.onTrade = g
t.onAckModifyOrders = h

t.run()

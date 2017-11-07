import tradersbot as tt
import time

t = tt.TradersBot(host='127.0.0.1', id='trader0', password='trader0')

print 'hhi'
def f(msg, order):
    print 'yooo'
    print msg
def g(msg, order):
    '''for trade in msg['trades']:
        print('YOOOO')
        print(trade)

        if trade['buy_order_id'] in trade_ids or trade['sell_order_id'] in trade_ids:
            print('INNN')
            print(portfolio)
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
    print msg'''
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

def i(msg, order):
    for k in msg:
        print k
    for k in msg['trader_state']:
        print k 
print('ble')
t.onMarketUpdate = f
t.onTrade = g
t.onAckModifyOrders = h
t.onTraderUpdate = i
t.run()
print 'hiie'

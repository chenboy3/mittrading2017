import tradersbot as tt

t = tt.TradersBot(host='127.0.0.1', id='trader0', password='trader0')

vals = ['EUR', 'USD', 'CHF', 'JPY', 'CAD']
pub = ['USDCAD', 'EURUSD', 'USDCHF', 'USDJPY']
dark = ['EURCAD', 'EURJPY', 'EURCHF', 'CHFJPY']
prices = {}

history = {} # ticker : [isBuy, quantity, token, price]
portfolio = {'USD': 100000.0, 'EUR': 0.0, 'CHF': 0.0, 'JPY': 0.0, 'CAD': 0.0}

TOKEN = 'GoXeDl_'
token_id = 0
past_tokens = set()

order_id = []
info = []



for v in vals:
	prices[v] = {}
	for vv in vals:
		prices[v][vv] = 0.0



def f(msg, order):
	# get the market data and update
	ticker = msg['market_state']['ticker']
	# use last as price for now, can use something more sophisticated
# like weighted mid later
	price = msg['market_state']['last_price']
	update(ticker, price)
	#printVals()
	#cancelOrders(order)
	print('iddddd')
	#for id in order_id:
	#	print(id)
	cancelOrders(order)
	print('nere')
	#if ticker == 'EURCAD':
	#makeTrade('EURUSD', True, 100, price, order)
	#makeTrade('EURCAD', True, 100, price, order)
	for d in dark:
		updateDark(d, prices, order)
	'''print('portfolio')
	for p in portfolio:
		print (p)
		print (portfolio[p])'''

def g(msg, order):
	for trade in msg['trades']:
		print('YOOOO')
		print(trade)

		if 'token' in trade and trade['token'] in past_tokens:
			print('INNN')
			first_ticker = trade['ticker'][0:3]
			sec_ticker = trade['ticker'][3:6]
			quantity = trade['quantity']
			price = trade['price']
			isBuy = trade['buy']
			if isBuy:
				portfolio[first_ticker] += quantity
				portfolio[second_ticker] -= quantity * price
			else:
				portfolio[first_ticker] -= quantity * price
				portfolio[second_ticker] += quantity

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
						if price > 0:
							print('yo')
							print(ticker, price * .999)
							makeTrade(ticker, True, 100, price * .99, order)
							makeTrade(ticker, False, 100, price * 1.01, order)



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
	global token_id
	if ticker not in history:
		history[ticker] = []
	token = generateToken()
	history[ticker].append([isBuy, quantity, token, price])
	order.addTrade(ticker, isBuy, quantity, price, token)
	'''print('tokensss')
	for t in past_tokens:
		print(t)'''


def generateToken():
	global token_id
	token = TOKEN + str(token_id)
	past_tokens.add(token)
	token_id += 1
	return token

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
	#	print(id)
	if 'orders' in msg:
		for k in msg['orders']:
			order_id.append(k['order_id'])
			#print('iiddd')
			#print(k['order_id'])
			info.append(k['ticker'])


t.onMarketUpdate = f
#t.onTrade = g
t.onAckModifyOrders = h

t.run()

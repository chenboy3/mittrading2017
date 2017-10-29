import tradersbot as tt

t = tt.TradersBot(host='127.0.0.1', id='trader0', password='trader0')

vals = ['EUR', 'USD', 'CHF', 'JPY', 'CAD']
pub = ['USDCAD', 'EURUSD', 'USDCHF', 'USDJPY']
dark = ['EURCAD', 'EURJPY', 'EURCHF', 'CHFJPY']
prices = {}


for v in vals:
	prices[v] = {}
	for vv in vals:
		prices[v][vv] = 0.0

def f(msg, order):
	#get the market data and update
	ticker = msg['market_state']['ticker']
	#use last as price for now, can use something more sophisticated
	#like weighted mid later
	price = msg['market_state']['last_price']
	update(ticker, price)
	printVals()
	for d in dark:
		updateDark(d, prices)

def updateDark(ticker, prices):
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


t.onMarketUpdate = f

t.run()
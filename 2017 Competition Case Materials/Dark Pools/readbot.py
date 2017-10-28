import tradersbot as tt

t = tt.TradersBot(host='127.0.0.1', id='trader0', password='trader0')

vals = ['EUR', 'USD', 'CHF', 'JPY', 'CAD']
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
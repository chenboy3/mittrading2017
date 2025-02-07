import tradersbot as tt
import math
import random
import requests
import json 

t = tt.TradersBot(host='127.0.0.1', id='trader0', password='trader0')
tick = 0
tickers = ['USDCAD','USDJPY','EURUSD','USDCAD','CHFJPY','EURJPY','EURCHF','EURCAD' ]

def get_side():
    return 'buy' if random.random() > 0.5 else 'sell'

def f(msg, order):    
    print(msg)
    print(len(msg))
    global tick
    quantity = 500
    
    idx = 'EURCAD'
    side = get_side()
    if side == 'buy':
        order.addBuy(idx, quantity=quantity, price=11.01)
        print('buy')
    else:
        order.addSell(idx, quantity=quantity, price=1.01) 

    tick += 1
    print('Traded')

def f2(msg, order):    
    global tick
    quantity = 500
    idx = 'EURCAD'
    side = get_side()
    if side == 'buy':
        order.addBuy(idx, quantity=quantity, price=0.99)
    else:
        order.addSell(idx, quantity=quantity, price=1.01) 

    tick += 1
    print('Traded')

t.onMarketUpdate = f
t.run()

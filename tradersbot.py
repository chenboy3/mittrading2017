from tradersbot import TradersBot
import requests
import json

t = TradersBot('18.247.12.164', 'trader0', 'trader0')

# sample callback functions

# submit market buy for 20 shares of AAPL
# if the first letter of the news body is 'T'
def buyApple(msg, order):
    newsBody = msg["news"]["body"]
    if len(newsBody) > 0 and newsBody[0] == 'T':
        order.addBuy('AAPL', 20)

# don't forget this line!
t.onNews = buyApple

######################################################
# each time AAPL trade happens for $x, make bid
# and ask at $x-0.02, $x+0.02, respectively
def marketMake(msg, order):
    for trade in msg["trades"]:
        if trade["ticker"] == 'AAPL':
            px = trade["price"]
            order.addBuy('AAPL', 10, px - 0.02)
            order.addSell('AAPL', 10, px + 0.02)
t.onTrade = marketMake

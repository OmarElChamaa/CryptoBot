#!/usr/bin/env python3

import os
import csv
import math

from binance.enums import *
from binance.exceptions import BinanceAPIException, BinanceOrderException
from binance.websockets import BinanceSocketManager
from twisted.internet import reactor
from binance.client import Client
### Welcome Interface #
print ('Welcome to CryptoPump by DK--\n')


##
api_key=input('Type in your api Key :')
api_secret=input('Type in your api Key secret :')
client = Client(api_key,api_secret)
# client.API_URL = 'https://testnet.binance.vision/api'
print(client.get_system_status())



##
print('Your current balances For BTC,USDT,BNB : (Free are usable, Locked are in orders) ')
print(client.get_asset_balance(asset='BTC'))
print(client.get_asset_balance(asset='BNB'))
print(client.get_asset_balance(asset='USDT'))

### Crypto Used For buying
buy_currency = "BTC"
percent_of_wallet=1.0
gainz=1.5
stop_loss=0.55

print(client.get_asset_balance(asset=buy_currency))
wallet_balance=client.get_asset_balance(asset=buy_currency)['free']

crypto_to_buy = input('\n\nThe crypto that you want to PUMP !! IN CAPITALS!!: (LAST STEP BEFORE PUMP!!)\n')
market=crypto_to_buy+buy_currency
print("Market is %s "%market)


#default value to round if symbol not found

def round_down(n, decimals=0):
    multiplier = 10 ** decimals
    return math.floor(n * multiplier) / multiplier




try:
    precision = client.get_symbol_info(market)
    print(precision['filters'])
    fraction =precision['filters'][2]['minQty']
    print("Min qty to buy is : " + fraction)
    
    after_decimal=fraction.index("1")
    
    if after_decimal>0:
        after_decimal-1

    print("after decimal : %d" %after_decimal)
except TypeError as e: 
    print(e)

info=client.get_symbol_ticker(symbol=market)
current_price=info['price']
print("current price:"+current_price)

total_buying=(float(wallet_balance)*percent_of_wallet)
print("Buying with %s" % total_buying)



print("BUY--------------------------------------------------------------\n")
try: 
    
    number=(float(wallet_balance)*percent_of_wallet)/float(current_price)
    number=round_down(number,after_decimal)
    number=str(number)
    print("Quantity of crypto to buy " + number)
    
    
    order = client.order_limit_buy(
        symbol=market,
        quantity=number,
        price=current_price)
    
    print(order)
except BinanceAPIException as e:
    # error handling goes here
    print(e)
except BinanceOrderException as e:
    # error handling goes here
    print(e)

    

sell_limit_price=float(current_price)*gainz
sell_limit_price="{:.8}".format(sell_limit_price)
print(sell_limit_price)
print("sell limit price after round:" + sell_limit_price)



sell_stop_loss=float(current_price)*stop_loss
sell_stop_loss="{:.8f}".format(sell_stop_loss)
print(type(sell_stop_loss))


sell_stop_loss_limit=float(sell_stop_loss)*0.90
sell_stop_loss_limit="{:.8f}".format(sell_stop_loss_limit)



try:
    order = client.create_oco_order(
        symbol=market,
        side='SELL',
        quantity=number,
        price=sell_limit_price,
        stopPrice=sell_stop_loss,
        stopLimitPrice=sell_stop_loss_limit,
        stopLimitTimeInForce='GTC')

    print("OCO order---------------------------------------------\n")
    print(order)

except BinanceAPIException as e:
    # error handling goes here
    print(e)
except BinanceOrderException as e:
    # error handling goes here
    print(e)


input("Press enter to exit ;")


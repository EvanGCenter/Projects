## Program for interfacing with binance to check all coin value activity and 
## finding crossings where a shorter term SMA becomes greater than a longer 
## term SMA, indicating an upcoming bullish period for the coin

## import packages 
from binance.client import Client
import talib
import datetime
import numpy as np
import captainCoinKeys #script containing your Binance API information
# import matplotlib.pyplot as plt

## variables that we might want to change later
current_time = datetime.datetime.now() #get current date
ndays = 365 #length of data to import
SMA_long = 99 #long term simple moving average window
SMA_short = 25 #short term SMA window
cross_window = -18 #number of recent days to find crossing
date_range = datetime.timedelta(days = ndays)
active_window = current_time - date_range

## login using Binance API
apiKey = captainCoinKeys.apiKey
apiSecurity = captainCoinKeys.apiSecurity

client = Client(apiKey, apiSecurity)
print ("logged in")

# infoClient = client.get_account()

# bal = infoClient['balances']
# for b in bal:
#     if float(b['free']) > 0:
#         print(b)
        
## get the data for all bitcoin pairs and tidy it
bin_products = client.get_products()
bin_data = bin_products['data'] 
btc_pairs = [pair['s'] for pair in bin_data if pair['s'].endswith("BTC")]

candle_data = [client.get_historical_klines(pair, Client.KLINE_INTERVAL_1DAY, str(active_window)) for pair in btc_pairs]

close_data = np.zeros((len(btc_pairs),ndays)) #get close data and discard the rest
for token in range(len(candle_data)):
    for day in range(len(candle_data[token])):
        close_data[token][day] = candle_data[token][day][4]

## calculate short and long SMAs
SMA_long_data = np.zeros((len(btc_pairs),ndays))
SMA_short_data = np.zeros((len(btc_pairs),ndays))
for token in range(len(close_data)):
    SMA_long_data[token] = talib.SMA(close_data[token],SMA_long)
    SMA_short_data[token] = talib.SMA(close_data[token],SMA_short)
   
## run the analysis to find the crossings and add relevant coins to stonk list
stonks = []
for comp in range(len(btc_pairs)):
    if SMA_short_data[comp][cross_window] < SMA_long_data[comp][cross_window]:
        if SMA_short_data[comp][-1] > SMA_long_data[comp][-1]:
           stonks.append(btc_pairs[comp])
           
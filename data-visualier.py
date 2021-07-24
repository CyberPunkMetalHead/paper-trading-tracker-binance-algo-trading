import json
from binance.client import Client
from binance.exceptions import BinanceAPIException
from datetime import datetime

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

client = Client()


sns.set_style('darkgrid') # darkgrid, white grid, dark, white and ticks
sns.set_context("poster")
plt.rc('axes', titlesize=18)     # fontsize of the axes title
plt.rc('axes', labelsize=14)    # fontsize of the x and y labels
plt.rc('xtick', labelsize=13)    # fontsize of the tick labels
plt.rc('ytick', labelsize=13)    # fontsize of the tick labels
plt.rc('legend', fontsize=13)    # legend fontsize
plt.rc('font', size=13)          # controls default text sizes

def load_trades(data):
    with open(data, 'r') as f:
        return json.load(f)


def get_data(symbol, since):
    return client.get_historical_klines(symbol, Client.KLINE_INTERVAL_1DAY, since)


def get_daily_close(data):

    daily_close = {}

    for coin in data:
        time = datetime.fromtimestamp(data[coin]['time'])
        time = time.strftime("%d %B, %Y")

        daily_close[coin] = get_data(data[coin]['symbol'], time )
        daily_close[coin] = [[item[4] for item in daily_close[coin]], [datetime.fromtimestamp(item[0]/1000) for item in daily_close[coin]]]

    return daily_close


def get_buy_price(data):
    buy_price = {}
    for coin in data:
        buy_price[coin] = data[coin]['price']

    return buy_price


def daily_pnl(close, buy_price):
    daily_pnl = {}

    for coin in close:
        daily_pnl[coin] = []
        for price in close[coin][0]:
            daily_pnl[coin].append(((float(price) - float(buy_price[coin])) / float(buy_price[coin])*100 ))
    return daily_pnl


def get_total_pnl(data):
    avg_pnl = {}
    for coin in data:
        print(coin)
        if len(data[coin]) >0:
            avg_pnl[coin] = round(data[coin][-1],3)

    total_pnl = sum([avg_pnl[item] for item in avg_pnl]) / len(avg_pnl)

    return avg_pnl, total_pnl


def main():

    trades = load_trades('order.json')
    daily_close = get_daily_close(trades)

    buy_price = get_buy_price(trades)

    pnl = daily_pnl(daily_close, buy_price)
    print(pnl)

    avg_pnl, total_pnl = get_total_pnl(pnl)
    print(avg_pnl, total_pnl)

    for coin in pnl:
        #plt.plot(pnl[coin], label=coin)
        plt.legend()
        #fig, ax = plt.subplots()
        #plt.plot(daily_close[coin][1], pnl[coin], label=coin)
        plt.scatter(daily_close[coin][1], pnl[coin], label=coin)
        plt.legend()
        plt.xlabel('Date')
        plt.ylabel('Percentage Change')



    plt.show()

if __name__ == '__main__':
    main()

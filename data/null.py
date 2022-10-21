# Bitcoin Data
# Measuring hash rates --> measures energy usage of the blockchain

import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
import matplotlib.dates as mdates
import numpy as np
import os

def average_hash_rates(df): #returns map of average hash rates for years 2009 - 2022
    m = {} # year : array of hash-rates
    for index,row in df.iterrows(): 
        year = row["timestamp"][:4] #year
        hash_rate = row["hash-rate"]
        if year not in m: 
            m[year] = []
        m[year].append(hash_rate)

    averages = {}
    for key, val in m.items():
        avg = sum(val)/len(val)
        averages[key] = avg

    return averages

def average_market_price(df): # returns map of average market price for years 2009 - 2022
    m = {}
    for index, row in df.iterrows():
        year = row["timestamp"][:4]
        price = row["market-price"]
        if year not in m:
            m[year] = []
        m[year].append(price)

    averages = {}
    for key, val in m.items():
        avg = sum(val)/len(val)
        averages[key] = avg
    return averages

def plot_hash_rate(df,df2):
    year = df['timestamp'].to_numpy()
    year = [dt.datetime(int(yr[:4]), int(yr[5:7]), int(yr[8:10])) for yr in year] #removing timestamps and only having dates
    hashrate = df['hash-rate'].to_numpy()
    plt.plot(year, hashrate, label = "Hash-Rate")
    plt.legend()
    plt.title("Bitcoin Energy Usage")
    plt.xlabel("Year")
    plt.ylabel("Hash-Rate (hashes/second)")

    plt.show()


def plot_hash_rate_vs_market_price(df, df2):
    
    year = df['timestamp'].to_numpy()
    year = [dt.datetime(int(yr[:4]), int(yr[5:7]), int(yr[8:10])) for yr in year] #removing timestamps and only having dates
    hashrate = df['hash-rate'].to_numpy()

    year2 = df2['timestamp'].to_numpy()
    year2 = [dt.datetime(int(yr[:4]), int(yr[5:7]), int(yr[8:10])) for yr in year2] #removing timestamps and only having dates
    market = df2['market-price'].to_numpy()

    fig, ax = plt.subplots()
    ax.plot(year, hashrate, label = "Hash-Rate", color = "red")
    
    ax.set_xlabel("Year")
    ax.set_ylabel("Hash-Rate (MW)", color = "red")
    
    ax2 = ax.twinx()
    ax2.plot(year2, market, label = "Market-Price",color = "blue")
    ax2.set_ylabel("Market-Price ($)", color = "blue")
    
    plt.title("Market Price & Bitcoin Energy Usage")
    
    plt.show()

def plot_market_price(df):
    year = df['timestamp'].to_numpy()
    year = [dt.datetime(int(yr[:4]), int(yr[5:7]), int(yr[8:10])) for yr in year] #removing timestamps and only having dates
    hashrate = df['market-price'].to_numpy()
    plt.plot(year, hashrate, label = "market-price")
    plt.title("Bitcoin Market Price")
    plt.xlabel("Year")
    plt.ylabel("Market Price")
   # plt.show()
    
def plot_power_req_per_cryptonetwork(df):
    # P (power requirement per cryptonetwork) = HR(hashes/second) x PE(Joules/ Hash) x 2.78x10^{-10} x 3600
    # using power efficiency of a mining machine in 2017

    m = average_hash_rates(df)
    years, averages = [], []
    for yr, avg in m.items():
         years.append(yr)
         averages.append(avg)
    
    x = .15 * 2.78 * 10**(-10) * 3600
    averages = [avg * x for avg in averages]
    plt.bar(years, averages, label = 'Power')
    plt.legend()
    plt.title('Power Requirement of Bitcoin Network (2009-2022)')
    plt.xlabel('Year')
    plt.ylabel('Power (MegaWatts)')
    plt.show()
        

if __name__ == "__main__": 
    all_time_hash_rates_df = pd.read_csv("data/bitcoin-all-time-hash-rate.csv")
    all_time_market_price_df = pd.read_csv("data/bitcoin-all-time-market-price.csv")
    

    hash_rate_averages = average_hash_rates(all_time_hash_rates_df)
    market_prices = average_market_price(all_time_market_price_df)
    
    #print average hash rates for years 2009 -- 2022     -->     Energy bitcoin uses
    # for key,val in hash_rate_averages.items(): 
    #     print("Year",key, " --> ", val)
    
    #print market price for years 2009 - 2022
    # for key,val in market_prices.items():
    #     print("Year",key, " --> ",val)


    #plots: 

    #plot average hash rates 2009 - 2022
    # plot_hash_rate(all_time_hash_rates_df)
    # plt.show()
    #plot market price for years 2009 - 2022
    # plot_market_price(all_time_market_price_df)
    # plt.show()


    
    # 2017-2018 .015 JH^-1 

    # P (power requirement per cryptonetwork) = HR(hashes/second) x PE(Joules/ Hash) x 2.78x10^{-10} x 3600 
    # ends up being the same because multiplied by constants --> I could multiply power efficiency with average per each year. 
    plot_power_req_per_cryptonetwork(all_time_hash_rates_df)
    plot_hash_rate(all_time_hash_rates_df, all_time_market_price_df)
    plot_hash_rate_vs_market_price(all_time_hash_rates_df, all_time_market_price_df)
    #  Network velocity ($ Us per hour)




    
    
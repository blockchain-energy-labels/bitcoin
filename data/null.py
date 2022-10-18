# Bitcoin Data
# Measuring hash rates --> measures energy usage of the blockchain

import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
import matplotlib.dates as mdates
import numpy as np
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
    # years, values = [] , []
    # for index,row in df.iterrows():
    #     year = row["timestamp"][:10]
    #     val = row["hash-rate"]
    #     years.append(year)
    #     values.append(val)

    # return years, values

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

def plot_hash_rate(df):
    year = df['timestamp'].to_numpy()
    year = [dt.datetime(int(yr[:4]), int(yr[5:7]), int(yr[8:10])) for yr in year] #removing timestamps and only having dates
    hashrate = df['hash-rate'].to_numpy()
    plt.plot(year, hashrate, label = "Hash-Rate")
    plt.title("hash rate vs year all time")
    plt.xlabel("year")
    plt.ylabel("hashrate")
   # plt.show()


def plot_market_price(df):
    year = df['timestamp'].to_numpy()
    year = [dt.datetime(int(yr[:4]), int(yr[5:7]), int(yr[8:10])) for yr in year] #removing timestamps and only having dates
    hashrate = df['market-price'].to_numpy()
    plt.plot(year, hashrate, label = "market-price")
    plt.title("market price vs year all time")
    plt.xlabel("year")
    plt.ylabel("marketp rice")
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
    plt.bar(years, averages, label = 'power required')
    plt.title('power for cryptonetwork by year')
    plt.xlabel('year')
    plt.ylabel('power (megawatts)')

    

    
    # year = df['timestamp'].to_numpy()
    # year = [dt.datetime(int(yr[:4]), int(yr[5:7]), int(yr[8:10])) for yr in year] #removing timestamps and only having dates
    # hashrate = df['hash-rate'].to_numpy()
    #implement above equation for Pß
    # x = .15 * 2.78 * 10**(-10) * 3600 #2017 power efficiency included in equation
    # power = [hr * x for hr in hashrate]
    # plt.plot(year, power, label = "power required")
    # plt.title("power required")
    # plt.xlabel("year")
    # plt.ylabel("power")
        
        



if __name__ == "__main__": 
    all_time_hash_rates_df = pd.read_csv("/Users/devanshuhaldar/Desktop/RPI/Blockchain-Energy-Labels/bitcoin/data/bitcoin-all-time-hash-rate.csv")
    all_time_market_price_df = pd.read_csv("/Users/devanshuhaldar/Desktop/RPI/Blockchain-Energy-Labels/bitcoin/data/bitcoin-all-time-market-price.csv")
    

    hash_rate_averages = average_hash_rates(all_time_hash_rates_df)
    market_prices = average_market_price(all_time_market_price_df)
    
    #print average hash rates for years 2009 -- 2022     -->     Energy bitcoin uses
    # for key,val in hash_rate_averages.items(): 
    #     print("Year",key, " --> ", val)
    
    #print market price for years 2009 - 2022
    # for key,val in market_prices.items():
    #     print("Year",key, " --> ",val)




    #plots: 

    # #plot average hash rates 2009 - 2022
    # plot_hash_rate(all_time_hash_rates_df)
    # plt.show()
    # #plot market price for years 2009 - 2022
    # plot_market_price(all_time_market_price_df)
    # plt.show()


    
    # 2017-2018 .015 JH^-1 

    # P (power requirement per cryptonetwork) = HR(hashes/second) x PE(Joules/ Hash) x 2.78x10^{-10} x 3600 
    # ends up being the same because multiplied by constants --> I could multiply power efficiency with average per each year. 
    plot_power_req_per_cryptonetwork(all_time_hash_rates_df)
    plt.show()
    #  Network velocity ($ Us per hour)




    
    
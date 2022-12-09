# Bitcoin Data
# Measuring hash rates --> measures energy usage of the blockchain

from locale import D_FMT
from re import L
from sre_parse import State
from time import strftime
import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
import matplotlib.dates as mdates
import numpy as np
import statistics 
import json
import csv 

# Hash Rate correlates to energy usage
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

#market price. values required for future calculations
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

#Plots hash rate 2009 - 2022
def plot_hash_rate(df):
    year = df['timestamp'].to_numpy()
    hashrate = df['hash-rate'].to_numpy()
    
    year = [dt.datetime(int(yr[:4]), int(yr[5:7]), int(yr[8:10])) for yr in year] #removing timestamps and only having dates

    plt.plot(year, hashrate, label = "Hash-Rate")
    plt.legend()
    plt.title("Bitcoin Energy Usage")
    plt.xlabel("Year")
    plt.ylabel("Hash-Rate (hashes/second)")
   # plt.show()

#Plots hash rate compared to market price 2009 - 2022
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
    


# Amount of US $ generated per hour
def plot_network_velocity(df):
    year = df['timestamp'].to_numpy()
    year = [dt.datetime(int(yr[:4]), int(yr[5:7]), int(yr[8:10])) for yr in year] #removing timestamps and only having dates
    market = df['market-price'].to_numpy()

    temp = 6.25/6 #coin reward per block / # of blocks generated per hour
    market = [price * temp for price in market]

    plt.plot(year,market,label = "network velocity")
    plt.title("Bitcoin Network Velocity (2009-2022)")
    plt.xlabel("Year")
    plt.ylabel("Network Velocity (US $ per Hour)")
    #plt.show()

    return year, market

#plots market price 2009 - 2022
def plot_market_price(df):
    year = df['timestamp'].to_numpy()
    hashrate = df['market-price'].to_numpy()
    
    year = [dt.datetime(int(yr[:4]), int(yr[5:7]), int(yr[8:10])) for yr in year] #removing timestamps and only having dates
    
    plt.plot(year, hashrate, label = "market-price")
    plt.title("Bitcoin Market Price")
    plt.xlabel("Year")
    plt.ylabel("Market Price")
    #plt.show()
    
    
def calculate_power(df): #returns list of power for each date
    year = df['timestamp'].to_numpy()
    year = [dt.datetime(int(yr[:4]), int(yr[5:7]), int(yr[8:10])) for yr in year] #removing timestamps and only having dates
    hashrate = df['hash-rate'].to_numpy()
    temp = .15 * 2.78 * 10**(-10) * 3600
    powers = [p * temp for p in hashrate] # for other functions such as generation of 1 US dollar
    return year, powers

#plots power requirement averages of cryptonetwork
def plot_power_averages(df):
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
    

def plot_generate_USD(year1,year2,velocity,powers):
    # Energy required for 1 US dollar
    # Power / Velocity * 3600
    year2 = year2[3:]
    velocity = velocity[3:]
    res = []

    for i in range(len(year1)):
        res.append(powers[i]/velocity[i] * 3600) 

    plt.plot(year1, res)
    plt.title("Energy Required to Generate 1 USD")
    plt.xlabel("Year")
    plt.ylabel("Energy (MegaJewels/US$)")
   # plt.show()
    

def calculate_N_c(year, P): #function to support plot_daily_energy and carbon emission by state. Calculates values for daily energy required 
    x = 6/6.25 * 1000 #blocks generated per hour * energy supply /coins mined per block
    res = [p * x for p in P]
    return res

def plot_daily_energy(year, P):
    #P * t_b (how many blocks generated per hour) * 1000 / 6.25      t_b = 6
    res = calculate_N_c(year,P)
    
    csvarr = []            #       to create a csv for js files
    for i in range(len(year)):
        csvarr.append((year[i].date(),res[i]))
    pd.DataFrame(csvarr).to_csv("daily_energy_coin_csv", index = False)

    plt.plot(year, res)
    plt.title("Daily Energy to Produce a Coin")
    plt.xlabel("Year")
    plt.ylabel("Energy (KWH/Coins Mined)")
    plt.show()
    

# uses carbon factors from 2021 for each state
# len(states) = len(carbon_factors)
def plot_carbon_emission_states(states,co2): #carbon factor --> lbs/kWH
    plt.bar(states,co2)
    plt.xlabel("States")
    plt.ylabel("Co2 Emitted (lbs)")
    plt.title("Co2 Emitted Per BitCoin Mined")
    plt.show()
    



if __name__ == "__main__": 
    all_time_hash_rates_df = pd.read_csv("data/bitcoin-all-time-hash-rate.csv")
    all_time_market_price_df = pd.read_csv("data/bitcoin-all-time-market-price.csv")
    state_emission_factors_df = pd.read_csv("data/state_emission_factor.csv")

    hash_rate_averages = average_hash_rates(all_time_hash_rates_df)
    market_prices = average_market_price(all_time_market_price_df)

    #PLOTS: 

    # plot average hash rates 2009 - 2022
    # plot_hash_rate(all_time_hash_rates_df)
    
    #plot market price for years 2009 - 2022
    #plot_market_price(all_time_market_price_df)
    
    year1, powers = calculate_power(all_time_hash_rates_df)
    plot_hash_rate_vs_market_price(all_time_hash_rates_df, all_time_market_price_df)

    
    #Network velocity ($ Us per hour)
    year2, market = plot_network_velocity(all_time_market_price_df)
    

    # Energy required for 1 US dollar
    plot_generate_USD(year1, year2, market, powers)
    

    #daily energy required to produce a coin on a given day 
    plot_daily_energy(
        year1,powers)
    

    #  Carbon emissions 
    # states, carbon_factor, co2 = [], [], []
    # for index, row in state_emission_factors_df.iterrows():
    #     states.append(row["State"])
    #     carbon_factor.append(row["lbs/kWH"])
    
    # N_c = calculate_N_c(year1, powers)
    # N_c = statistics.median(N_c)

    
    # for i in range(len(states)):
    #     co2.append(carbon_factor[i] * N_c )
    # plot_carbon_emission_states(states,co2) #carbon emitted in lbs per coin mined

    # state_dict_value = {}
    # total = 0
    # for i in range(len(states)):
    #     state_dict_value[states[i]] = co2[i]
    #     total += co2[i]

    # state_dict_percent = {}
    # for i in range(len(states)):
    #     state_dict_percent[states[i]] = co2[i]/total
    #     print(states[i], ",", co2[i]/total)



    #Convert data arrays into two column csv files
    # csvarr = []            #       to create a csv for js files
    # for i in range(len(year1)):
    #     csvarr.append((year1[i].date(),res[i]))
    # pd.DataFrame(csvarr).to_csv("energy_req_usd_csv", index = False)
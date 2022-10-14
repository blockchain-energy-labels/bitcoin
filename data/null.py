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

def show_average_hash_rate(year,hashrate):
    plt.bar(year,hashrate, label = 'Hash-Rate')
    plt.title('Hashrate Avg per Year')
    plt.xlabel('Year')
    plt.ylabel('Hash Rate (100 million)')
    plt.show()
        
        



if __name__ == "__main__": 
    all_time_hash_rates_df = pd.read_csv("csv location")
    all_time_market_price_df = pd.read_csv("csv location")


    hash_rate_averages = average_hash_rates(all_time_hash_rates_df)
    market_prices = average_market_price(all_time_market_price_df)
    
    #print average hash rates for years 2009 -- 2022     -->     Energy bitcoin uses
    # for key,val in hash_rate_averages.items(): 
    #     print("Year",key, " --> ", val)
    
    #print market price for years 2009 - 2022
    # for key,val in market_prices.items():
    #     print("Year",key, " --> ",val)

    #merge = pd.DataFrame({'date' : hash_rate_averages[0], 'hash-rate' : hash_rate_averages[1]})
    # merge["date"] = pd.to_datetime(merge["date"])
    # df1 = merge.groupby(merge["date"].dt.to_period("M")).sum()
    # df1 = df1.resample("M").asfreq().fillna(0)
    # df1.plot(kind = 'bar')
    # plt.show()
    # print(merge["date"])
    # year = int(merge["date"][0][:4])
    # day = int(merge["date"][0][5:7])
    # month = int(merge["date"][0][8:10])
    # year2 = int(merge["date"][len(merge["date"])-1][:4])
    # day2 = int(merge["date"][len(merge["date"])-1][5:7])
    # month2 =int(merge["date"][len(merge["date"])-1][8:10])
    # dates = mdates.drange(dt.datetime(year, month, day), dt.datetime(year2, month2, day2), dt.timedelta(days = 1))
    # fig, ax = plt.subplots()
    # width = np.diff(dates).min()
    # counts = merge['hash-rate'].to_numpy()
    # print(len(dates))
    # print(len(counts))
    # ax.bar(dates,counts, align= 'center',width = width)
    # ax.xaxis_date()
    # fig.autofmt_xdate()
    # plt.show()  
    
 


    # df['date'] = pd.to_datetime(df['date'])
    # df1 = df.groupby(df['date'].dt.to_period('M')).sum()
    # df1 = df1.resample('M').asfreq().fillna(0)
    # df1.plot(kind='bar')



    year = []
    hashrate = []
    for yr, hr in hash_rate_averages.items():
        year.append(yr)
        hashrate.append(hr)
    show_average_hash_rate(year,hashrate)
    
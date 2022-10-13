# Bitcoin Data
# Measuring hash rates --> measures energy usage of the blockchain

import pandas as pd


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




        
        



if __name__ == "__main__": 
    all_time_hash_rates_df = pd.read_csv("/Users/devanshuhaldar/Desktop/RPI/Blockchain-Energy-Labels/Bitcoin/data/bitcoin-all-time-hash-rate.csv")
    all_time_market_price_df = pd.read_csv("/Users/devanshuhaldar/Desktop/RPI/Blockchain-Energy-Labels/Bitcoin/data/bitcoin-all-time-market-price.csv")


    hash_rate_averages = average_hash_rates(all_time_hash_rates_df)
    market_prices = average_market_price(all_time_market_price_df)
    
    #print average hash rates for years 2009 -- 2022     -->     Energy bitcoin uses
    # for key,val in hash_rate_averages.items(): 
    #     print("Year",key, " --> ", val)

    #print market price for years 2009 - 2022
    # for key,val in market_prices.items():
    #     print("Year",key, " --> ",val)

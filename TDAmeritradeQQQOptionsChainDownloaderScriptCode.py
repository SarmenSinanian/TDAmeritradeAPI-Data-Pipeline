import requests
import pandas as pd
import pickle
from Config import ConsumerKey as key
from datetime import date

# define our endpoint
endpoint = r'https://api.tdameritrade.com/v1/marketdata/chains'

# definte our payload
payload = {'apikey': key,
           'symbol': 'QQQ',
           'strikeCount': '30',
           'fromDate': '2022-04-01'}

# make a request
content = requests.get(url=endpoint, params=payload)

# convert it to a dictionary
data = content.json()

optionsChain = pd.json_normalize(data)

categories = ['putCall', 'symbol', 'volatility', 'delta', 'gamma',
              'theta', 'vega', 'rho', 'totalVolume', 'openInterest', 'strikePrice']

selected = pd.DataFrame(columns=categories, dtype=object)

for i in range(len(optionsChain.transpose()) - 12):
    for j in categories:
        # iterate and put values into 'selected' dataframe
        selected.at[i, j] = optionsChain.iat[0, i + 12][0].get(j)

# create set for use with dataFrame creation loop (name of dfs = date portion of 'symbol')
dateSet = []
for i in selected['symbol']:
    if i[4:10] not in dateSet:
        a = i[4:10]
        dateSet.append(a)

# creating dataframes via loop with names = items from dateSet above
d = {}
for name in dateSet:
    d[name] = pd.DataFrame(columns=categories, dtype=object)

# loop through all dateSet dates, then loop through all rows in selected(dataframe),
#  check if date from dateSet is within symbol from current row of selected(dataframe),
#  if date from dateSet is within symbol from current row of selected(dataframe) then add the
#  current row of selected(dataframe) into the dateSet dates' dataframe (dataframes are housed
#  within the 'd' dictionary which is a dictionary of dataframes created for each date)
for dates in dateSet:
    counter = 0
    for symbol in selected['symbol']:
        if dates in symbol:
            d[dates].loc[len(d[dates].index)] = selected.loc[counter]
        counter += 1

currentDay = date.today()

today = str(currentDay.month) + str(currentDay.day) + str(currentDay.year)

# Checking if single digit date and adding zeros accordingly; formatting entire date properly
if len(str(currentDay.day)) == 1:
    correctedDay = str(currentDay.day).zfill(2)
else:
    correctedDay = currentDay.day

if len(str(currentDay.month)) == 1:
    correctedMonth = str(currentDay.month).zfill(2)
else:
    correctedMonth = currentDay.month

today = str(correctedMonth) + str(correctedDay) + str(currentDay.year)

try:
    with open('mypickle.pickle', 'rb') as f:
        bigDictionary = pickle.load(f)
except Exception as e:
    print(e)

# Iteratively adding dictionaries per day
bigDictionary[today] = d

with open('mypickle.pickle', 'wb') as f:
    pickle.dump(bigDictionary, f, protocol=pickle.HIGHEST_PROTOCOL)
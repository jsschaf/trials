'''Predict Outcomes of 2021 USA Olympic Swimming Men 100 Free'''


from datetime import datetime
from statistics import mean, median
import matplotlib.pyplot as plt
import matplotlib.dates as dts
import numpy as np
import pandas as pd
import csv

trialdate= dts.date2num(np.datetime64('2021-06-16'))

datetime.strptime('2012-02-10' , '%Y-%m-%d')

df = pd.read_csv('formatted_times.csv')
df = df.drop('Unnamed: 0', 1)

times = {}

def plot_swimmer(seasons, swimmer):
    i=0
    cols = ['b', 'g', 'r', 'c', 'm', 'k']
    for season in seasons:

        xTemp, yTemp = seasons[season]['Dates'], seasons[season]['Times']

        plt.plot(xTemp, yTemp, marker='.', linestyle="", color=cols[i] )
        if (season != 2020) and (len(xTemp) != 0):
            #plot the line of best fit
            mTemp, bTemp = np.polyfit(xTemp, yTemp, 1)
            mxTemp = []
            for k in range(len(xTemp)):
                mxTemp.append(mTemp*xTemp[k])
            
            plt.plot(xTemp, mxTemp + bTemp, color=cols[i])
            plt.xlabel("Season")
            plt.ylabel("Time")
            i += 1
            
    ax = plt.gca()
    labs = (ax.get_xticks())
    swag = []
    for elt in labs:
        swag.append(dts.num2date(elt).strftime('%Y'))

    ax.set_xticklabels(swag)
    plt.savefig(swimmer + '.jpg')
    

def predictSwimmer(swimmerTimes, swimmer):
    dates, times = zip(*swimmerTimes)
    times = [x for _, x in sorted(zip(dates, times))]

    df = pd.DataFrame(swimmerTimes, columns =['Date', 'Time'])
    df = df.sort_values(by=['Date'])

    #find one seasons linear regression
    seasons = {}
    for i in range(2015,2021):
        seasons[i] = {"Dates":[], "Times":[]}

    for _, row in df.iterrows():
        date = (row['Date'])
        time = row['Time']
        season_year = date.year
        if date.month < 9:
            #season belongs to prior year
            season_year = date.year - 1

        seasons[season_year]['Dates'].append(date)
        seasons[season_year]['Times'].append(time)

    #tentatively remove covid season
    seasons.pop(2019)
    gradients = []

    for season in seasons:

        x, y = seasons[season]['Dates'], seasons[season]['Times']
        for j in range(len(x)):
            x[j] = dts.date2num(np.datetime64(x[j]))

        if (season != 2020) and (len(x) != 0):
            #plot the line of best fit
            m, b = np.polyfit(x, y, 1)
            mx = []
            for k in range(len(x)):
                mx.append(m*x[k])
            gradients.append(m)

    lineOfBestFitPreds = []
    if len(gradients) != 0:
        for l in range(len(seasons[2020]['Dates'])):
            # find prediction using average of past gradients
            # take point in middle of 2020 season
            time20 = (seasons[2020]['Times'][l])
            date20 = (seasons[2020]['Dates'][l])
            # y = mx + b
            # b = y - mx
            intercept = time20 - (mean(gradients)*date20)
            # now predict on olympic trial date
            trialtime = (mean(gradients)*(trialdate)) + intercept
            lineOfBestFitPreds.append(trialtime)
    if len(lineOfBestFitPreds) != 0:
        predict1 = median(lineOfBestFitPreds)
    fastest = []
    # find fastest times each season

    years = []
    for year in seasons:
        if (year != 2020) and (len(seasons[year]['Times']) != 0):
            fastest.append(min(seasons[year]['Times']))
            years.append(year)
    PB = 0
    if (len(fastest) != 0):
        PB = min(fastest)
        print(PB)
    if len(years) != 0:
        m2, b2 = np.polyfit(years, fastest, 1)
        predict2 = (m2*2020) + b2

        if len(lineOfBestFitPreds) == 0:
            return predict2
        predictedTime = mean([predict1, predict2])
        # cap it at PB of 1.5s
        # todo --> change 1.5 to whatever the biggest PB of 2016 & 2012 was 
        if (PB - predictedTime) > 1.5:
            return PB - 1.5
        return predictedTime
    # swimmer has never before made it
    # need to predict based on this years times only
    
    # if only one date, predict same result
    if len(seasons[2020]['Dates']) == 0:
        print('ONE TIME ONLY')
        return seasons[2020]['Times']
    m3, b3 = np.polyfit(seasons[2020]['Dates'], seasons[2020]['Times'], 1)
    predict3 = m3*trialdate + b3
    return predict3

# Create Dict to track all times for each swimmer
for row in df.itertuples():
    time = float(row[2][2:].replace('"',''))
    date = row[3][2:].replace('"','')
    date = datetime.strptime(date, '%m/%d/%Y').date()
    if(row[1]) not in times:
        times[row[1]] = [(date, time)]
    else:
        times[row[1]].append((date, time))

predictions = {}
for swimmer in times:
    print(swimmer)
    predictions[swimmer] = predictSwimmer(times[swimmer], swimmer)

with open('predictions.csv', 'w') as csv_file:  
    writer = csv.writer(csv_file)
    for key, value in predictions.items():
       writer.writerow([key, value])


# TODO WHY IS JACK SO FAST
# PB IS ONLY 50.0
'''Predict Outcomes of 2021 USA Olympic Swimming Men 100 Free'''


from datetime import datetime
from statistics import mean, median
import matplotlib.pyplot as plt
import matplotlib.dates as dts
import numpy as np
import pandas as pd
import csv
import itertools 

trialdate= dts.date2num(np.datetime64('2021-06-16'))
datetime.strptime('2012-02-10' , '%Y-%m-%d')

def predictPastTrends(season2020, aveGradient):
    lineOfBestFitPreds = []
    for l in range(len(season2020['Dates'])):
        # find prediction using average of past gradients
        # take point in middle of 2020 season
        time20 = (season2020['Times'][l])
        date20 = (season2020['Dates'][l])
        # y = mx + b
        # b = y - mx
        intercept = time20 - (aveGradient*date20)
        # now predict on olympic trial date
        trialtime = (aveGradient*(trialdate)) + intercept
        lineOfBestFitPreds.append(trialtime)
    if(min(season2020['Times']) - median(lineOfBestFitPreds) > 1.5):
        return (min(season2020['Times']) - 1.5)
    return median(lineOfBestFitPreds)

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
            plt.locator_params(axis='x', nbins=7)
            plt.title('100 Freestyle: ' + swimmer)
            plt.xlabel("Date")
            plt.ylabel("Time")
            i += 1
            
    ax = plt.gca()
    labs = (ax.get_xticks())
    swag = []
    for elt in labs:
        swag.append(dts.num2date(elt).strftime('%m/%Y'))

    ax.set_xticklabels(swag)
    plt.savefig(swimmer + '.jpg')
    plt.close()
   
def predictFastest(seasons):

    fastest = []
    years = []
    for year in seasons:
        if (year != 2020) and (len(seasons[year]['Times']) != 0):
            fastest.append(min(seasons[year]['Times']))
            years.append(year)

    
    gradient, intercept = np.polyfit(years, fastest, 1)

    # gradient = average amount person drops per season
    # predicted time = latest PB - gradient
    pred2 = fastest[-1] + gradient
    diff = []
    for i in range(len(fastest) - 1):
        diff.append(fastest[i] - fastest[i+1])

    #predictedTime = (gradient*2020) + intercept
    
    PB = min(fastest)
    if (PB - pred2) > 1.5:
        return PB - 1.5
        
    return pred2 # predictedTime

def seasonTransform(df):
    
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
    
    return seasons

def findGradients(seasons):
    gradients = []
    for season in seasons:

        x, y = seasons[season]['Dates'], seasons[season]['Times']
        for j in range(len(x)):
            x[j] = dts.date2num(np.datetime64(x[j]))
        # if there is more than one swim, we can create a line of best fit
        if (season != 2020) and (len(x) > 1):
            #plot the line of best fit
            m, b = np.polyfit(x, y, 1)
            mx = []
            for k in range(len(x)):
                mx.append(m*x[k])
            gradients.append(m)
    
    return gradients

def pastSwims(seasons):
    
    if(len(seasons[2015]['Dates']) > 0):
        return True
    if(len(seasons[2016]['Dates']) > 0):
        return True
    if(len(seasons[2017]['Dates']) > 0):
        return True
    if(len(seasons[2018]['Dates']) > 0):
        return True
    return False
    
def predictSwimmer(swimmerTimes, swimmer):

    df = pd.DataFrame(swimmerTimes, columns =['Date', 'Time'])
    df = df.sort_values(by=['Date'])
    
    #transform data to be order by swimming season
    seasons = seasonTransform(df)

    # find average slop of past seasons swims
    gradients = findGradients(seasons)
    
    # if there have been past swims and there are current season swims, make prediction
    if ((len(gradients) != 0) and (len(seasons[2020]['Dates']) > 0)):
        gradientPrediction = predictPastTrends(seasons[2020], mean(gradients))
    # find fastest times each season
    # plot here?
    #    plot_swimmer(seasons, swimmer)
    
    #find fastest swims each year
    # if there have been swims in past years
    if(pastSwims(seasons)):
        fastestPrediction = predictFastest(seasons)

        # if we have a gradient prediction also - then use mean
        if (len(gradients) != 0) and (len(seasons[2020]['Dates']) > 0):
            return mean([gradientPrediction, fastestPrediction])
        
        #we dont have a gradient prediction
        return fastestPrediction
    
    # swimmer has never before made it
    # need to predict based on this years times only

    # if only one date, predict same result
    if len(seasons[2020]['Dates']) == 1:
        return seasons[2020]['Times']

    # predict based on this years linear trend only
    m3, b3 = np.polyfit(seasons[2020]['Dates'], seasons[2020]['Times'], 1)
    predict3 = m3*trialdate + b3
    return predict3

def run(event):


    df = pd.read_csv('data/' + event + '.csv')
    df = df.drop('Unnamed: 0', 1)

    times = {}  
    # Create Dict to track all times for each swimmer
    for row in df.itertuples():
        #adjust float calc if event is 200s
        if event[1] == '2':
            ntime = row[2][2:].replace('"','')
            ptime = float(row[2][2:].replace('"','')[2:])

            if (ntime[0] == '1'):
                ptime += 60.0
            else:
                ptime += 120.0

            time = ptime
        else:
            time = float(row[2][2:].replace('"',''))
        date = row[3][2:].replace('"','')
        date = datetime.strptime(date, '%m/%d/%Y').date()
        if(row[1]) not in times:
            times[row[1]] = [(date, time)]
        else:
            times[row[1]].append((date, time))

    predictions = {}


    for swimmer in times:
        predictions[swimmer] = predictSwimmer(times[swimmer], swimmer)
        
    predictions = dict(sorted(predictions.items(), key=lambda item: item[1]))
    with open('results/' + event + 'predictions.csv', 'w') as csv_file:  
        writer = csv.writer(csv_file)
        
        for key, value in predictions.items():
            if event[1] == '2':
                if value > 120:
                    if value < 130:
                       value = "2:0" + str(value-120) 
                    else:
                        value = "2:" + str(value-120)
                else:
                    value = "1:" + str(value-60)
                value = value[:7]
            else:
                value = str(value)[:5]
            writer.writerow([key, value])

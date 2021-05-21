import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt


datetime.strptime('2012-02-10' , '%Y-%m-%d')

df = pd.read_csv('formatted_times.csv') 
df = df.drop('Unnamed: 0', 1)

times = {}

# Create Dict to track all times for each swimmer
for row in df.itertuples():
    time = float(row[2][2:].replace('"',''))
    date = row[3][2:].replace('"','')
    date = datetime.strptime(date, '%m/%d/%Y').date()
    if(row[1]) not in times:
        times[row[1]] = [(date, time)]
    else:
        times[row[1]].append((date, time))
        
test = times['Dressel, Caeleb']
dates, times = zip(*test)
times = [x for _, x in sorted(zip(dates, times))]
plt.plot(sorted(dates), times)
plt.ylabel('Times')
plt.show()


# todo : create line graph sample
# todo : create Shiskin decomposition of one sample


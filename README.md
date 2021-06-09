# trials
Predicting the 100m free at 2021 USA Olympic Swimming Trials

### Run.py
Execute complete program using:s
> python run.py

This will produce predictions for mens and womens 100 and 200 freestyles and output results in the results/ directory.

### Transform.py

Using the usaswimming.org database:
1. Gather all Olympic Trials free qualifiers (m100_qual.csv)
2. Gather all times (faster than B standard) swum in USA since 1 September 2015 (m100_june.csv).
3. Remove all swims for those not qualified for Olympic Trials
4. Save output to new csv file (m100.csv). 

### Predict.py
For each swimmer, predict outcome of a chosen event. 


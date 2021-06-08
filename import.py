import pandas as pd

# Import names of Olympic Trials Qualifiers
df = pd.read_csv('mwave1200.csv', usecols=['="full_name"', '="foreign_yesno"']) 
df = df[df['="foreign_yesno"'] != '="Yes"']
qualifiers = df['="full_name"'].unique()
data = pd.read_csv('mjune8200.csv')

# Import all times
data.columns=data.columns.str.replace('[", =]','')
data = data[data.foreign_yesno != '="Yes"']
data = data[~data.swim_time_formatted.str.contains('r')]
data.drop(['distance', 'result_rank', 'time_id', 'meet_name', 'standard_name', 'foreign_yesno', 'event_desc', 'alt_adj_swim_time_formatted', 'swimmer_age', 'club_name', 'hytek_power_points', 'lsc_id', 'swimmer_age', 'event_id', 'sanction_status'], axis=1, inplace=True)

# Remove people that have not qualified for Trials
data = data[data['full_name'].isin(qualifiers)]

# Saving CSV of all relevant times for 2021 OT Qualifiers
data.to_csv('mformatted_timesjune8200.csv')
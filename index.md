## Predicting the Results of USA Swimming Olympic Trials

With Wave 2 of USA Swimming Olympic Trials around the corner, levels of spectator speculation are reaching all-time highs. In an attempt to join the join the fun, and potentially have some long-awaited pickem’ success, I have attempted to predict race outcomes using the available data on usaswimming.org and a bit of programming.![image](https://user-images.githubusercontent.com/25021191/121615015-47527b80-caa3-11eb-8995-200446b8433a.png)


### The Data:

Let’s focus on predicting a few marquee events which will impact USA Relays in Tokyo: The Men’s and Women’s 100 and 200 Freestyle events.  

To keep the analysis relatively recent and manageable, data used was from the beginning of the 2015/2016 season up until June 7, 2021. All athletes qualified for the 2021 USA Olympic Trials (Wave 1 and 2) were considered given that no start lists were available at the time of writing. 

### The Method:
Each swimmer had their performances broken down into seasons:
```markdown
-	2015/16
-	2016/17
-	2017/18
-	2018/19
-	2020/21
```
The 2019/2020 season was not included due to Covid-19 interruptions.

Each swimmer had their performance plotted, an example of Caeleb Dressel’s 100 Free shown here:
```markdown
![Dressel 100 Free](https://github.com/jsschaf/trials/blob/gh-pages/Dressel%2C%20Caeleb.jpg)
```
The gradient of each season’s linear progression was used to find an expected slope for the current season. In other words, we can look at how much faster or slower a swimmer typically gets throughout the season and apply that information to the current season. To continue the Dressel example, he typically gets steadily faster as a season progresses, and ends up between 2.5 and 3.5 seconds faster at the end of the season than the beginning. 
Using linear regression with this predicted slope and the times already swum this season, we can project a 2021 Olympic Trial result. 

This result was cross referenced with the trends of season-best performances since 2015. For example, if a swimmer has season best times of 50.0, 49.5, 49.0 in each of the last 3 seasons, we predict they will swim a 48.5 in the following season. Admittedly, this does not perfectly represent the nuances of dropping time in one’s swimming career. 


This analysis attempts to consider the overall trend of a swimmer’s improvement, their tendency to drop time at taper, as well as the actual times they have been recently swimming. It does not consider external factors that are ultimately also at play, such as sickness or injury, experience, nerves, or covid related training difficulties. However, it does provide a useful and fun point of analysis, highlighting some exciting ‘up and comers’ that have been rising the ranks and could make a big impact at trials. 

### The Results (top 30):

#### Men 100 Free

| Place | Name | Time |
| --- | --- | --- |
| 1	| Dressel, Caeleb	| 47.06 |
|2	|Apple, Zach	|47.48|
|3|	Howard, Robert|	47.69|
|4	|Rooney, Maxime	|47.83|
|5	|Held, Ryan|	47.98|
|6	|Smith, Kieran	|47.99|
|7	|Farris, Dean	|48.00|
|8	|Jackson, Tate|	48.03|
|9	|Pieroni, Blake|	48.10|
|10	|Theall, Mark	|48.32|
|11	|Seliskar, Andrew|	48.38|
|12	|Casas, Shaine	|48.41|
|13	|Molacek, Jacob	|48.50|
|14	|Adrian, Nathan	|48.55|
|15	|Maurer, Luke	|48.64|
|16	|Stewart, Coleman|	48.69|
|17	|Alexy, Jack	|48.77|
|18	|Chadwick, Michael	|48.81|
|19	|Krueger, Danny	|48.86|
|20	|Newkirk, Jeff	|48.94|
|21	|Pinfold, Brett	|48.97|
|22	|Conger, Jack	|49.10|
|23	|Kibler, Drew	|49.12|
|24	|Delakis, Paul|	49.20|
|25	|Wright, Colin|	49.22|
|26	|Lasco, Destin|	49.25|
|27	|Curry, Brooks|	49.26|
|28	|Loy, Drew	|49.29|
|29	|Shebat, John|	49.29|
|30|	Chaney, Adam|	49.32|


#### Men 200 Free

#### Women 100 Free

#### Women 200 Free

# Online Evaluation

We will determine the performance of our system while it is deployed based on the following factors:
- online evaluation metric (which we will define and explain below)
- response time of the API

## Online evaluation metric

Usually, online evaluation involves A/B tests which means there should be another recommendation model to compare our recommendation with (as we do not have access to ground truth). But in our case, instead of contrasting and comparing our recommendations with another model, we instead looked at the logs and the ratings from the user in real time. Our rationale was something along the lines of the phenomenon observed while watching youtube. Say, the user is watching some video and he/she gets a bunch of recommendations and they may also get asked "what do you think about this recommendation?". Borrowing from that idea we thought, what if we look at the logs in real time to check for the ratings and latest watch history of the user.

So our online evaluation works like this: We look at the latest ratings provided by a user. We also collect the data on what proportion of the movie is watched. Then we compare them with what our recommendation is and calculate a score for each recommendation. Lastly, we record the response time to get this recommendation and record this to track the performance across a random sample of users.

This approach makes sure that we make use of the telemetry information provided from the logs (in real systems, we presume there will more details available in the telemetry data including user behavior on the website, which is not present in the available logs. But we do have information on watchtime and ratings which we use.)

### How did we work with real time data?
To work with the log data in real time, we found that utilising promtail (logs forwarding), loki (log aggregationn) and grafana (visualisation) is clever solution. Intially, we were using these tools for log collection and monitoring but we discovered that they can be exposed over API to gain access to the log data so that it can be used as dataset which being updated in the real time from kafka stream. So, we wrote wrapper for the above mentioned tools to send API requests with the queries we wanted to obtain the results for our online processing.

### Calculation involved?

#### Scoring recommendation list
- If the sample-movie lies in the top 5: score = 10/10
- If the sample-movie lies in the top 6-10: score = 8/10
- If the sample-movie lies in the top 11-15: score = 5/10
- If the sample-movie lies in the top 16-20: score = 3/10
- If the sample-movie does nit lie in the recommended list: score = 0.01/10

#### Scoring ratings
The users would have given some rating to the movie: (score/5)

#### Scoring runtime
Based on how much of the movie the user has watched.
```
    [0-20%):    1/5
    [20-50%):   3/5
    [50-70%):   4/5
    [70-100%]:  5/5
```
#### Final calculation
We wanted to capture how the user is perceiving our recommendations:
i) Depending on how much of the movie was watched: Recommended_list_score x runtime_score
ii) what rating was given: Recommended_list_score x Ratings_score

(i+ii): predicted movie scaled score to tell us appropriate the recommendation was.

#### What does the metric mean? How to interpret it?
Care was taken to ensure that we do not end up with zero values while multiplying the scores. 
We capture the following trends in our metric:
- How highly ranked was the sample-movie in the list of recommended movies or if the sample-movie was even part of the recommendation at all?
- What did the user feel about the movie? (captured by the rating they gave to the movie)
- Apart from feeling, how did the user actually act for that movie? (captured based on how much of the movie did they actually end up watching)
- How much time did we take to give our recommendation?

#### Special note
Originally we spend quite a bit of time to calculate the score for online evaluations as follows:

We looked at the latest ratings provided by the user. For that user and the movie combination, we looked at how much of the movie was watched by the user. Then we compared it with our recommendation. If the movie which the user rated high and watched a lot of was indeed part of our recommendation, then our recommendation was good.

This would have given us a single scaled score as follows: Recommended_list_score x Ratings_score x runtime_score = predicted movie scaled score to tell us appropriiate the recommendation was.

But **the problem** we faced with this approach was that we were limited by the LOKI API to get the result set for our queries to ratings and history view. This meant we could not access more than 5000 records at a time through the request in our code but we had the access to full history through directly getting the values in the grafana dashboard. The problem was that a common movie and user combination did not exist in the ratings and history view for the 5000 records we had access to in a single API request. We did not have the time to write a selenium script to bypass their restrictive limit. It is possible that since we are using free which is why we had this limitation. To overcome this, we changed our evaluation strategy such that it could work with rolling logs as described above.

#### Links to artifacts
[Online evaluation based on history](https://gitlab.cs.mcgill.ca/comp585_2023f/team-4/-/commit/5c5e121b6102908d30678242ef0907681089fcb1#33c123951964e87db9810f2101b3da7faf79bdac_0_50)

[Online evaluation based on ranking](https://gitlab.cs.mcgill.ca/comp585_2023f/team-4/-/commit/5c5e121b6102908d30678242ef0907681089fcb1#1da93171e07e7f05bbccd3f2241b707c694cf00e_0_50)
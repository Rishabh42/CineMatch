# Conceptual Analysis of Potential Problems
## Fairness

### Definition

In order to analyze the fairness of our model, it is important to define what we mean by fairness. In the scientific literature, there are numerous definitions of fairness, and a taxonomy of these definitions can be found in [this paper](https://dl.acm.org/doi/pdf/10.1145/3547333). The definition of fairness that we will use in our project is based on three principles:

- Our definition is **outcome-oriented**, meaning that it considers the fairness of the outputs of our model rather than the process.
- We evaluate fairness in relation to **groups of individuals** (for example, based on their gender, age, etc.) rather than the individuals themselves.
- Our definition is based on the concept of **Consistent Fairness**, meaning that two similar groups of individuals should be treated similarly. In the context of our project, this implies that two groups of people should have a similar quality of recommended outcomes, regardless of the social group to which they belong.

### Potential issue 1

A first issue that may arise is that our model does not have the same quality of recommendation depending on the social group to which an individual belongs. The quality of recommendations can be evaluated based on how close the model's predictions are to reality, so we can use the Root Mean Square Error (RMSE). To detect this problem, we can separate our test dataset into different social groups and compare the RMSE for each social group. For example, in the context of our project, we can assess differences in RMSE for each gender, age, and occupation.

### Potential issue 2

A second issue that can arise in the context of recommendation systems is that two groups of individuals may not have the same variety of recommended items. To address this, we can compare the variety of movies that a social group watches and compare it with the variety of recommendations provided. Two groups of individuals with the same variety of movie genres watched should have the same variety of genres in their recommendations.  To detect this problem, we can evaluate the variance of movie genres proposed in the recommendations for each social group and compare it to the variance of the movies watched by that group.

### Reduce potential issues

Issues of fairness often have numerous sources. First, we will discuss one source that can lead to fairness problems: the dataset. Our recommendation system relies on the proximity between users, whether through our demographic filter grouping individuals by social groups or our collaborative filter, which is also influenced by the demographics of individuals because our tastes often align with those of people in the same social groups. Consequently, if we have too little data on a particular social group, the quality and variety of recommendations for that group may be poorer. It is crucial to have a diverse and representative dataset. Note that the dataset should not only contain sufficient data for all social groups but also for all intersections of social groups. One way to address this issue would be to collect more data on social groups with less data.

The lack of variety in our system's recommendations can also be attributed to the implementation of our model. Our model includes a demographic filter that acts solely based on a person's gender. This can lead to gender stereotyping of recommendations, especially if combined with an imbalanced dataset between the two genders, as the variety of films appreciated by one gender might be less well captured. One way to address this problem would be to consider additional demographic factors in our demographic filter.

## Feedback loop

### Potential issue 1 - Echo chamber

#### Description

The first feedback loop is called the "echo chamber". This feedback loop occurs when an item is highly recommended, leading to more users watching it. In the context of our model, this can happen because we consider the overall popularity of a movie to estimate its recommendation, and thus, movies that are generally well-liked are highly recommended.

The echo chamber can have both positive and negative consequences. The positive impact of this feedback loop is that most of the time, when a movie is liked by many users, there's a high probability that it will appeal to the majority of users. Consequently, it will appear in the recommendations of more and more users as it gains popularity.

But, if a movie becomes highly rated because it is extensively watched by a bubble of people who like that type of movie, it will then be propelled into everyone's recommendations, including those not particularly interested in that type of movie. With this movie repeatedly appearing in recommendations, even users who are not interested may eventually watch it. If it turns out not to be to their liking, they might give it a poor rating. The impact of this can vary depending on the recommendation model used: if the model primarily considers the number of people who have watched the movie, it might further boost its recommendations. However, if the model is based on ratings (like ours) or viewing time, the movie might cease to be recommended altogether, even to those who initially enjoyed that type of movie.

On the contrary, this can also lead to some movies never recommended. For instance, if a movie receives an initial poor rating, it may not appear in the recommendations for anyone and, consequently, never get watched, so never get rated again, etc.

#### Detection

This feedback loop can be detected by observing how the ratings of certain movies evolve based on how much they have been recommended. It's also crucial to examine which films are never recommended. Monitoring these patterns can provide insights into the presence and impact of the echo chamber feedback loop.

#### Mitigation

A solution to mitigate this is to place less emphasis on the popularity of a movie if the positive ratings come from users who have little resemblance (this can be assessed using the similarity matrix generated by collaborative filtering, for example), and to give it more weight if it comes from a bubble of people with similar tastes.

Another solution, especially to prevent movies from never being recommended, is to introduce a small element of randomness. This allows certain movies to have a second chance and be recommended to users, even if they haven't received high popularity or ratings initially.

### Potential issue 2 - Filter bubble

#### Description

The second feedback loop is the "Filter Bubble." This feedback loop occurs when a user's recommendations become increasingly personalized, showing the user only a very limited and homogeneous subset of all the films on the platform. 

The primary positive consequence of this feedback loop is that users will receive recommendations with a very high probability of enjoyment. However, the downside is that it confines users to a bubble where the content they consume is limited, giving them the impression that their preferences are generalizable to everyone. Moreover, these bubbles can be observed demographically and may contribute to reinforcing social biases. For example, a movie about a princess might be more recommended to little girls, thus reinforcing the social bias as it is more watched by them, even if little boys might like it too.

#### Detection

Analyzing the variety of films recommended to users and how it varies across user demographics can provide insights into the existence and impact of this type of feedback loop.

#### Mitigation

To mitigate this feedback loop, we can introduce a small element of randomization into everyone's recommendations. This helps recommend slightly more diverse types of films, breaking the homogeneity of personalized recommendations. Even though adding this random element may lead to a decrease in accuracy, it can also enable users to discover new interests. It strikes a balance between personalized recommendations and the exploration of diverse content.

# Analysis of Problems in log Data

## Fairness

### Dataset analysis

From our data analysis, it seems that social groups are distributed similarly between the ratings dataset and the users dataset. 

However, the distribution within the datasets is highly uneven between social groups themselves. As seen in the diagrams below, the dataset contains significantly more men than women, with the majority of individuals being between 24 and 35 years old, and students being much more represented than other occupations. 

We have also examined intersections of social groups. For example, we observed that, on average, women are older than men, and 11% of women are academics/educators compared to 2% of men. Regarding differences in occupations between women and men, we would like to emphasize that achieving balance in this intersection of social groups can be more complex than simply having a similar representation across occupations between women and men because a person's occupation is not an independent variable from their gender, unlike age and gender, which can be considered independent. 

<img src="https://gitlab.cs.mcgill.ca/comp585_2023f/team-4/-/raw/tamara-fairness-feedback-loop/app/fairness_feedbackloop_analysis/results/GenderDistribution.png" alt="GenderDistribution" width="500"/>

<img src="https://gitlab.cs.mcgill.ca/comp585_2023f/team-4/-/raw/tamara-fairness-feedback-loop/app/fairness_feedbackloop_analysis/results/AgeDistribution.png" alt="AgeDistribution" width="500"/>

<img src="https://gitlab.cs.mcgill.ca/comp585_2023f/team-4/-/raw/tamara-fairness-feedback-loop/app/fairness_feedbackloop_analysis/results/MenOccupationDistribution.png" alt="MenOccupationDistribution" width="500"/>

<img src="https://gitlab.cs.mcgill.ca/comp585_2023f/team-4/-/raw/tamara-fairness-feedback-loop/app/fairness_feedbackloop_analysis/results/WomenOccupationDistribution.png" alt="WomenOccupationDistribution" width="500"/>

You can find all the statistics and results of our analysis [here](https://gitlab.cs.mcgill.ca/comp585_2023f/team-4/-/tree/tamara-fairness-feedback-loop/app/fairness_feedbackloop_analysis/results) (in particular, the results of all the groups intersections), and the code to generate these results [here](https://gitlab.cs.mcgill.ca/comp585_2023f/team-4/-/blob/tamara-fairness-feedback-loop/app/fairness_feedbackloop_analysis/data_fairness.py).

### Quality of recommendations

We then analyzed the differences in the quality of recommendations based on gender, age, and occupation. After training our model on the train dataset, we divided the test dataset according to the gender, age, and occupation of the users, calculating the RMSE for these sub-datasets of the test dataset. 

We then displayed our results in the graphs below. We can observe that while there is only a small difference in RMSE between women and men, the disparity in RMSE is much greater when calculated based on age or occupation. The explanation for this could be that our demographic filter only takes into account the gender, and not other demographic factors such as age or occupation. Expanding the demographic filter to include these additional factors may help address the observed disparities in RMSE across different age groups and occupations. 

We notice also that for age, the less data we have for an age group, the more heterogeneous the RMSE is.

<img src="https://gitlab.cs.mcgill.ca/comp585_2023f/team-4/-/raw/tamara-fairness-feedback-loop/app/fairness_feedbackloop_analysis/results/RmsePerGender.png" alt="RmsePerGender" width="500"/>

<img src="https://gitlab.cs.mcgill.ca/comp585_2023f/team-4/-/raw/tamara-fairness-feedback-loop/app/fairness_feedbackloop_analysis/results/RmsePerAge.png" alt="RmsePerAge" width="500"/>

<img src="https://gitlab.cs.mcgill.ca/comp585_2023f/team-4/-/raw/tamara-fairness-feedback-loop/app/fairness_feedbackloop_analysis/results/RmsePerOccupation.png" alt="RmsePerOccupation" width="500"/>

You can find all the statistics and results of our analysis [here](https://gitlab.cs.mcgill.ca/comp585_2023f/team-4/-/tree/tamara-fairness-feedback-loop/app/fairness_feedbackloop_analysis/results), and the code to generate these results [here](https://gitlab.cs.mcgill.ca/comp585_2023f/team-4/-/blob/tamara-fairness-feedback-loop/app/fairness_feedbackloop_analysis/quality_fairness.py).

## Feedback loop

We decided to analyze the Echo Chamber feedback loop. To gather a new dataset of ratings and examine how ratings have evolved since the implementation of our model, we calculated the average ratings for each movie in our initial training set and in the new dataset we have just collected. We then compare the evolution of the ratings:

In an [Excel spreadsheet](https://gitlab.cs.mcgill.ca/comp585_2023f/team-4/-/blob/tamara-fairness-feedback-loop/app/fairness_feedbackloop_analysis/results/mean_rating_by_movie.ods), we compared the correlation between the ratings given to these movies in our training dataset and the difference (both absolute and non-absolute) in the average ratings these movies received between the beginning of the semester and now. We have observes correlations, but these can be explained by an other factor than the Echo Chamber feedback loop. 

For example, we observe a very significant negative correlation when comparing with the non-absolute difference with the previous mean of ratings (r = -0.61221059, p = 3.0293E-250). This means that the most liked films are the ones that have lost the most in popularity, and the least liked films are the ones that have gained the most in popularity. However, this can be explained by the fact that movies that are nearly rated 5/5 have little room for improvement, and movies that are nearly rated 1/5 have little room for deterioration.

You can find the implementation of this part [here.](https://gitlab.cs.mcgill.ca/comp585_2023f/team-4/-/blob/tamara-fairness-feedback-loop/app/fairness_feedbackloop_analysis/feedback_loop.py)

# Contribution

Conceptual Analysis of Potential Problems: Tamara ([commit 1](https://gitlab.cs.mcgill.ca/comp585_2023f/team-4/-/commit/b337f8a6c6b9565cc590b93b24d70722e7a4d16a), [commit 2](https://gitlab.cs.mcgill.ca/comp585_2023f/team-4/-/commit/c735919017e60e0d04d48bc38883593fbc80f45b), [commit 3](https://gitlab.cs.mcgill.ca/comp585_2023f/team-4/-/commit/47a61d3aaa15621b9b6357110f2915e1998e2aee), ... (all the commits on the report))
Analysis of Problems in log Data: Tamara ([commit 1](https://gitlab.cs.mcgill.ca/comp585_2023f/team-4/-/commit/ed660124e3f4c9a6f9ab8a409dbf37f8ca927d82), [commit 2](https://gitlab.cs.mcgill.ca/comp585_2023f/team-4/-/commit/3f58aa15fd5634996b2b7cab4ff8fe2eac7ab226), [commit 3](https://gitlab.cs.mcgill.ca/comp585_2023f/team-4/-/commit/775c04af41486b0e8bfaec325bf3a4b8596981e2), [commit 4](https://gitlab.cs.mcgill.ca/comp585_2023f/team-4/-/commit/f9fdac273fb4bac7896abf21905c0b520e5d53c0))

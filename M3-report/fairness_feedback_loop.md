# Conceptual Analysis of Potential Problems
## Fairness

#### Definition

In order to analyze the fairness of our model, it is important to define what we mean by fairness. In the scientific literature, there are numerous definitions of fairness, and a taxonomy of these definitions can be found in [this paper](https://dl.acm.org/doi/pdf/10.1145/3547333). The definition of fairness that we will use in our project is based on three principles:

- Our definition is **outcome-oriented**, meaning that it considers the fairness of the outputs of our model rather than the process.
- We evaluate fairness in relation to **groups of individuals** (for example, based on their gender, age, etc.) rather than the individuals themselves.
- Our definition is based on the concept of **Consistent Fairness**, meaning that two similar groups of individuals should be treated similarly. In the context of our project, this implies that two groups of people should have a similar quality of recommended outcomes, regardless of the social group to which they belong.

#### Potential issue 1

A first issue that may arise is that our model does not have the same quality of recommendation depending on the social group to which an individual belongs. The quality of recommendations can be evaluated based on how close the model's predictions are to reality, so we can use the Root Mean Square Error (RMSE). To detect this problem, we can separate our test dataset into different social groups and compare the RMSE for each social group. For example, in the context of our project, we can assess differences in RMSE for each gender, age, and occupation.

#### Potential issue 2

A second issue that can arise in the context of recommendation systems is that two groups of individuals may not have the same variety of recommended items. To address this, we can compare the variety of movies that a social group watches and compare it with the variety of recommendations provided. Two groups of individuals with the same variety of movie genres watched should have the same variety of genres in their recommendations.  To detect this problem, we can evaluate the variance of movie genres proposed in the recommendations for each social group and compare it to the variance of the movies watched by that group.

#### Reduce potential issues

Issues of fairness often have numerous sources. First, we will discuss one source that can lead to fairness problems: the dataset. Our recommendation system relies on the proximity between users, whether through our demographic filter grouping individuals by social groups or our collaborative filter, which is also influenced by the demographics of individuals because our tastes often align with those of people in the same social groups. Consequently, if we have too little data on a particular social group, the quality and variety of recommendations for that group may be poorer. It is crucial to have a diverse and representative dataset. Note that the dataset should not only contain sufficient data for all social groups but also for all intersections of social groups. One way to address this issue would be to collect more data on social groups with less data.

The lack of variety in our system's recommendations can also be attributed to the implementation of our model. Our model includes a demographic filter that acts solely based on a person's gender. This can lead to gender stereotyping of recommendations, especially if combined with an imbalanced dataset between the two genders, as the variety of films appreciated by one gender might be less well captured. One way to address this problem would be to consider additional demographic factors in our demographic filter.
## Feedback loop


# Analysis of Problems in log Data

## Fairness

#### Quality of recommandations

#### Variety of recommandations

#### Dataset balance analysis

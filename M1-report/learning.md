For our movie recommender, we use collaborative filtering and other filtering techniques to produce the recommendation.

### Collaborative filtering

Collaborative filtering is a widely used technique in recommender systems based on the idea that the users who previously like the same movies in the past are more likely to like the same movies in the future. It estimates the similarities between the users and use it to produce the prediction. To compute the similarities, we use the k-nearest neighbors algorithm. 
We chose this technique because it is very popular for recommendation systems and allows us to have a good base that we can improve after.
To estimate how much a user liked a movie, we use the ratings given by that user.

### Cold start

To improve our algorithm, we decided to reduce the cold start problem. The cold start problem is one of the biggest problems of collaborative filtering: when a user has not yet given enough rates, the collaborative filter does not have enough data to find similar users. In case there is not enough data on a user, we decided to use their demographics data to find similar users and also the IMDB rating of the movies to recommend in priority the movies like in general.
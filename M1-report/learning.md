For our movie recommender, we use collaborative filtering and other filtering techniques to produce the recommendation.

### Collaborative filtering

Collaborative filtering is a widely used technique in recommender systems based on the idea that the users who previously liked the same movies in the past are more likely to like the same movies in the future. It estimates the similarities between the users and uses it to produce the prediction. To compute the similarities, we use the k-nearest neighbors algorithm with cosine similarity function.
We chose this technique because it is very popular for recommendation systems and allows us to have a good base that we can improve after.
To estimate how much a user liked a movie, we use the ratings given by that user.

### Cold start

To improve our algorithm, we decided to reduce the cold start problem. The cold start problem is one of the biggest problems of collaborative filtering: when a user has not yet given enough rates, the collaborative filter does not have enough data to find similar users. In case there is not enough data on a user, we decided to use their demographics data to find similar users and also the IMDB rating of the movies to recommend in priority the movies liked by everyone. For now, the only demographic info taken in account by our model is gender.

### Adult movie filter

We also put an adult movie filter that avoids recommending adult movies to kids.

### Implementation

For the implementation, we have used the python library Pandas for managing the databases, and Surprise for the machine learning part. 
Our model estimates the rates for all the movies the given user has not rated yet, and we take the 20 highest rates sorted in descending order. If the movie is an adult movie and the user is less than 18 years old, the predicted rate of the movie will be 0. If we have enough data to use collaborative filtering, we use the prediction of the collaborative filter, else the predicted rate will be based on the IMDB rate and the mean of the rates of this movies by user of the same gender.
Link to our model: 

### Limitations

Because there is a very large number of users, collective filtering requires a very large number of ratings to be effective. Collecting data from the stream takes time, so we did not have time to collect enough data for our model to be effective. Consequently, the majority of users suffer from the "cold start problem" because we do not have enough data on them. We therefore plan to retrain our model once we have collected more data.

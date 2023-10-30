# Offline evaluation

### Evaluation of the performance of the model

To evaluate the performance of the collaborative filtering model, we divided the dataset containing the ratings into two parts:
- A test dataset that corresponds to 20% of all ratings we have collected.
- A train dataset that corresponds to 80% of all ratings we have collected.
The model is then trained only on the train dataset. Then, we predict a rating with the model for each of the (user_id, movie_id) pairs present in the test dataset, and we calculate the Root Mean Squared Error between the list of predictions of the model and the list of real ratings present in the test dataset. Because the model was not trained on the data from the test dataset, we are know that RMSE is not biased by overfitting the test data. 

The Root Mean Squared Error measures the average difference between values predicted by a model and the actual values. We choose this performance indicators because it permits to know the average error that is made on predictions in general, which seemed to us to be the most relevant indicator. For example, this value can then be compared to the standard deviation of the rating dataset, which allows us to compare our predictor to a predictor which would always predict the average of the ratings. 

With our ratings dataset we have a Root Mean Squared Error of: 0.7215937657284225

### Unit tests

We also coded unit tests allowing us to see if the recommendations seemed at least coherent and which also allows us to test the other filters. For these unit tests, we created our own datasets, much smaller and simpler than the real datasets. Creating these small datasets allows us to have a better understanding of what is happening and to be able to more easily test simple cases. 

In these unit tests, we test:
- If a person under the age of 18, no film marked as "for adults" has been recommended to them (test for the adult filter)
- Verify that the recommendation includes 20 movies
- Verify that movies already rated by a user are not recommended to him/her again.
- Verify that a new user have also a list of 20 movies when he asks for recommendation.

We also test some functions used for our model in the unit tests:
- Verify that the model saves in the correct file.
- Verify that our helping function that print the results of the recommendation prints the result correctly.
- Verify that we load the entire dataset by checking the size.

### Links to the implementation:

Separation of the dataset into two parts and testing: https://gitlab.cs.mcgill.ca/comp585_2023f/team-4/-/blob/development/app/model/movie_rec.py
Unit tests and print the RMSE: https://gitlab.cs.mcgill.ca/comp585_2023f/team-4/-/blob/development/app/tests/model/test_model.py

# Data quality

We have done some unit test to be sure that the data is consistent. In these unit tests, we test:
- If all the user_ids in the ratings dataset are existing user_ids in the users dataset
- If all the movie_ids in the ratings dataset are existing movie_ids in the users dataset

Link to these unit tests: https://gitlab.cs.mcgill.ca/comp585_2023f/team-4/-/blob/development/app/tests/model/test_model.py

# Individual Contributions and Meeting Notes

**Offline evaluation:** Tamara

Relevant commit: 
- code: https://gitlab.cs.mcgill.ca/comp585_2023f/team-4/-/merge_requests/48/diffs?commit_id=25305ce70b22af98f74d5016fb3f8cee39fb8b99, https://gitlab.cs.mcgill.ca/comp585_2023f/team-4/-/commit/8ecc2a06f07426449d98ae65bcb4c4145754818d, https://gitlab.cs.mcgill.ca/comp585_2023f/team-4/-/commit/16e8ef354b7f3d2f9ca019401b157404c030933e, https://gitlab.cs.mcgill.ca/comp585_2023f/team-4/-/commit/691a68ba35fa361b0b876aa592dacb0fe5fc6f59, https://gitlab.cs.mcgill.ca/comp585_2023f/team-4/-/commit/d5be150108e8a9bf6b32326f390a53ac6a43b52f 
- report: https://gitlab.cs.mcgill.ca/comp585_2023f/team-4/-/merge_requests/48/diffs?commit_id=744759355d3f780d00f368a45364340fbae72b4f

**Data quality:** Aayush + some unit tests by Tamara

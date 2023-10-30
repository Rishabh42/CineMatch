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

# Pipeline:
We implemented an MLOps to get constant feedback during the development process and make sure that our code works seamlessly across different modules (data, ML model, app, etc.). 


## Pipeline structure:

We configured our pipeline to sequentially run the following different jobs/stages:
  - test-data
  - test-model
  - test-app
  - coverage
  - deploy

### Description of each stage:
- **test-data:** This pipeline runs tests on the data quality and data processing ensuring that the data which is being fed into the model is of good quality. 
  - It runs tests like checking if the movies are getting filtered, curl requests are working etc.  
  - Works on the following branches: main, development

- **test-model:** This pipeline runs tests on the model and ensures that functionalities like printing recommendations, test-train split, global dataset values etc. are working fine.     Based on these tests we get a good benchmark of our model performance.  
  - Works on the following branches: main, development.

- **test-app:** This pipeline runs tests on the flask app and ensures that functionalities like testing the endpoint of the flask app and other functions of the API are working fine.  
  - Works on the following branches: main, development

- **coverage:** We implemented a pipeline for the code coverage which tells us how much code of the app has been tested by the tests that we developed. 
  - This pipeline combines the results of all our tests described previously (data, model, app) and returns the final code coverage report. Currently our test coverage is at 91%.
  - Works on the following branches: main, development  
  - Link to our coverage report: ​​https://gitlab.cs.mcgill.ca/comp585_2023f/team-4/-/jobs/3699 

**Screenshot of our coverage report:**


- **deploy:** After all tests have passed, this final pipeline deploys our model and the app to our team server hosted on GitLab.  
Works on the following branches: main  
  - We set this job to work on only the `main` branch and not `development` as we don’t want to deploy a new model each time a new commit is pushed to development which is our final testing branch. Only when we are confident of our code we push to the `main` branch which deploys the model.  

**Reason why our testing is adequate:**  
As described above, we have tested the most crucial aspects of a machine learning model pipeline i.e. the data quality and the model performance. Additionally we have also tested the app interaction which makes our end-to-end test suite robust. \
\
**Links to our test suite and other test files:**
- https://gitlab.cs.mcgill.ca/comp585_2023f/team-4/-/tree/development/app/tests 
- https://gitlab.cs.mcgill.ca/comp585_2023f/team-4/-/blob/development/app/test_app.py 

**Reason for making the jobs sequential:**
We wanted to make sure that in case any of the jobs like `test-dat`, `test-model` and `test-app` fails, we don’t proceed forward unless we have fixed the issue concerned with the failing pipeline.

# Individual Contributions and Meeting Notes

**Offline evaluation:** Tamara

Relevant commit: 
- code: https://gitlab.cs.mcgill.ca/comp585_2023f/team-4/-/merge_requests/48/diffs?commit_id=25305ce70b22af98f74d5016fb3f8cee39fb8b99, https://gitlab.cs.mcgill.ca/comp585_2023f/team-4/-/commit/8ecc2a06f07426449d98ae65bcb4c4145754818d, https://gitlab.cs.mcgill.ca/comp585_2023f/team-4/-/commit/16e8ef354b7f3d2f9ca019401b157404c030933e, https://gitlab.cs.mcgill.ca/comp585_2023f/team-4/-/commit/691a68ba35fa361b0b876aa592dacb0fe5fc6f59, https://gitlab.cs.mcgill.ca/comp585_2023f/team-4/-/commit/d5be150108e8a9bf6b32326f390a53ac6a43b52f 
- report: https://gitlab.cs.mcgill.ca/comp585_2023f/team-4/-/merge_requests/48/diffs?commit_id=744759355d3f780d00f368a45364340fbae72b4f

**Data quality:** Aayush + some unit tests by Tamara


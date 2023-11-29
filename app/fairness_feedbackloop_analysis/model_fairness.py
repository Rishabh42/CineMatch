import os

import numpy as np
from matplotlib import pyplot as plt
from app.model.movie_rec import test_collaborative_filtering_subset, train

os.chdir("../")
CURR = os.getcwd()

MODEL_PATH = os.path.join(CURR, 'app', 'model', 'model.pkl')
DATA_PATH = os.path.join(CURR, 'app', 'data')
FILE_NAME_USERS = 'user_data.csv'
FILE_NAME_RATINGS = 'cleaned_rating.csv'
FILE_NAME_MOVIES = 'filtered_responses.csv'


def gender_rmse():
    return test_collaborative_filtering_subset('gender', ['M', 'F'])


def age_rmse():
    return test_collaborative_filtering_subset('age', range(0, 100))


if __name__ == '__main__':
    train(data_path=DATA_PATH, file_name_users=FILE_NAME_USERS, file_name_movies=FILE_NAME_MOVIES,
          file_name_ratings=FILE_NAME_RATINGS, model_path=MODEL_PATH)
    print(gender_rmse())
    print(age_rmse())

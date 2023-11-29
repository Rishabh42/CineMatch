import os

import numpy as np
from matplotlib import pyplot as plt
from app.model.movie_rec import test_collaborative_filtering_subset, train, load_dataset_from_csv

os.chdir("../")
CURR = os.getcwd()

MODEL_PATH = os.path.join(CURR, 'app', 'model', 'model.pkl')
DATA_PATH = os.path.join(CURR, 'app', 'data')
FILE_NAME_USERS = 'user_data.csv'
FILE_NAME_RATINGS = 'cleaned_rating.csv'
FILE_NAME_MOVIES = 'filtered_responses.csv'


def get_labels(column_name):
    data = load_dataset_from_csv(DATA_PATH, FILE_NAME_USERS, ['user_id', 'age', 'occupation', 'gender'])
    return data[column_name].unique().tolist()


def gender_rmse():
    return test_collaborative_filtering_subset('gender', get_labels('gender'))


def age_rmse():
    return test_collaborative_filtering_subset('age', get_labels('age'))


def occupation_rmse():
    return test_collaborative_filtering_subset('occupation', get_labels('occupation'))


if __name__ == '__main__':
    train(data_path=DATA_PATH, file_name_users=FILE_NAME_USERS, file_name_movies=FILE_NAME_MOVIES,
          file_name_ratings=FILE_NAME_RATINGS, model_path=MODEL_PATH)
    print(gender_rmse())
    print(age_rmse())
    print(occupation_rmse())

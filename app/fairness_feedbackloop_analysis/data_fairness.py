import os
from matplotlib import pyplot as plt
from app.model.movie_rec import load_dataset_from_csv

os.chdir("../")
CURR = os.getcwd()

DATA_PATH = os.path.join(CURR, 'app', 'data')
FILE_NAME_USERS = 'user_data.csv'


def dataset_gender_balance():
    data = load_dataset_from_csv(DATA_PATH, FILE_NAME_USERS, ['user_id', 'age', 'occupation', 'gender'])
    value_count = data['gender'].value_counts()
    plt.bar(value_count.index, value_count.values)
    plt.show()


if __name__ == '__main__':
    dataset_gender_balance()

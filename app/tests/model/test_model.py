import unittest
import os
import sys
from model.movie_rec import print_recommendations
from model.movie_rec import load_dataset_from_csv
from model.movie_rec import load_data
from model.movie_rec import train
from model.movie_rec import load_model
from model.movie_rec import get_recommendation

sys.path.append("..")
sys.path.append("..")

os.chdir("../")
CURR = os.getcwd()
MODEL_PATH = os.path.join(CURR, 'model', 'model.pkl')
DATA_PATH = os.path.join(CURR, 'tests', 'dummy_data_test')

FILE_NAME_USERS = 'simple_users.csv'
FILE_NAME_MOVIES = 'simple_movies.csv'
FILE_NAME_RATINGS = 'simple_ratings.csv'


class MyTestCase(unittest.TestCase):
    def test_print_recommendation(self):
        content_print = print_recommendations([('movie 1', 5), ('movie 2', 4), ('movie 3', 3)], 'user_id')
        expected_header = 'Top 3 Movie Recommendations for User user_id:'
        expected_line_1 = 'Movie ID: movie 1, Predicted Rating: 5.00'
        expected_line_2 = 'Movie ID: movie 2, Predicted Rating: 4.00'
        expected_line_3 = 'Movie ID: movie 3, Predicted Rating: 3.00'
        expected_string = expected_header + '\n' + expected_line_1 + '\n' + expected_line_2 + '\n' + expected_line_3
        self.assertEqual(content_print, expected_string)

    def test_global_dataset_columns_names(self):
        dataset = load_dataset_from_csv(DATA_PATH, 'simple_movies.csv', ['movie_id', 'adult', 'type', 'max_min',
                                                                         'global_rate', 'languages'])
        columns = dataset.columns.tolist()
        self.assertEqual(len(dataset.columns), 6)
        self.assertEqual(dataset.columns.tolist(), ['movie_id', 'adult', 'type', 'max_min', 'global_rate', 'languages'])

    def test_global_dataset_values(self):
        dataset = load_dataset_from_csv(DATA_PATH, 'simple_movies.csv', ['movie_id', 'adult', 'type', 'max_min',
                                                                         'global_rate', 'languages'])
        self.assertEqual(len(dataset), 30)
        self.assertEqual(dataset['movie_id'].tolist()[:3], ['movie1', 'movie2', 'movie3'])
        self.assertEqual(dataset['adult'].tolist()[:3], [False, False, True])
        self.assertEqual(dataset['type'].tolist()[:3], ['Romance, Comedy, Crime, Fantasy', 'Crime, Drama, Comedy',
                                                        'Drama'])
        self.assertEqual(dataset['max_min'].tolist()[:3], [101, 180, 93])
        self.assertEqual(dataset['global_rate'].tolist()[:3], [6.6, 7.9, 7.3])
        self.assertEqual(dataset['languages'].tolist()[:3], ['svenska, English', 'FranÃ§ais, English', 'EspaÃ±ol'])

    def test_size_load_data(self):
        dataset, users, users_ratings, movies = load_data(DATA_PATH, file_name_users=FILE_NAME_USERS,
                                                          file_name_movies=FILE_NAME_MOVIES,
                                                          file_name_ratings=FILE_NAME_RATINGS)
        self.assertEqual(len(users), 30)
        self.assertEqual(len(movies), 30)
        self.assertEqual(len(users_ratings), 81)
        self.assertEqual(len(dataset.df), 81)

    def test_users_are_the_same_load_data(self):
        dataset, users, users_ratings, movies = load_data(DATA_PATH, file_name_users=FILE_NAME_USERS,
                                                          file_name_movies=FILE_NAME_MOVIES,
                                                          file_name_ratings=FILE_NAME_RATINGS)
        # verify that the users are the same in the users_ratings and users
        self.assertEqual(users_ratings.merge(users, on='user_id')['user_id'].drop_duplicates().tolist(),
                         users_ratings['user_id'].drop_duplicates().tolist())
        # verify that the users are the same in the dataset and users
        self.assertEqual(dataset.df.merge(users, on='user_id')['user_id'].drop_duplicates().tolist(),
                         dataset.df['user_id'].drop_duplicates().tolist())

    def test_movies_are_the_same_load_data(self):
        dataset, users, users_ratings, movies = load_data(DATA_PATH, file_name_users=FILE_NAME_USERS,
                                                          file_name_movies=FILE_NAME_MOVIES,
                                                          file_name_ratings=FILE_NAME_RATINGS)
        # verify that the movies are the same in the dataset and movies
        self.assertEqual(dataset.df.merge(movies, on='movie_id')['movie_id'].drop_duplicates().tolist(),
                         dataset.df['movie_id'].drop_duplicates().tolist())

    def test_train_create_model(self):
        train(data_path=DATA_PATH, file_name_users=FILE_NAME_USERS, file_name_movies=FILE_NAME_MOVIES,
              file_name_ratings=FILE_NAME_RATINGS)
        self.assertTrue(os.path.exists(MODEL_PATH))

    def test_get_recommendation_not_recommend_movies_already_rated(self):
        train(data_path=DATA_PATH, file_name_users=FILE_NAME_USERS, file_name_movies=FILE_NAME_MOVIES,
              file_name_ratings=FILE_NAME_RATINGS)
        load_model(data_path=DATA_PATH, file_name_users=FILE_NAME_USERS, file_name_movies=FILE_NAME_MOVIES,
                   file_name_ratings=FILE_NAME_RATINGS)
        prediction = get_recommendation(2)
        self.assertNotIn('movie1', prediction)
        self.assertNotIn('movie19', prediction)
        self.assertNotIn('movie29', prediction)
        self.assertNotIn('movie30', prediction)


if __name__ == '__main__':
    unittest.main()

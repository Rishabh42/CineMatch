from surprise import Dataset, Reader
from surprise.model_selection import train_test_split
from surprise import KNNBasic
from surprise import accuracy
import pandas as pd
import numpy as np


def column_switch(column):
    if column['max_min'] != 0:
        return (column['min'] * 100) // column['max_min']
    return 0


def load_data(file_path):
    users = pd.read_csv('..\\data\\user_data.csv', sep=',', error_bad_lines=False, encoding="latin-1")
    users.columns = ['user_id', 'age', 'occupation', 'gender']

    ratings = pd.read_csv('..\\data\\cleaned_rating.csv', sep=',', error_bad_lines=False, encoding="latin-1")
    ratings.columns = ['user_id', 'movie_id', 'rate']
    users_ratings = pd.merge(ratings, users, on='user_id')

    history = pd.read_csv('..\\data\\movie_cleaned_1.csv', sep=',', error_bad_lines=False, encoding="latin-1")
    history.columns = ['user_id', 'movie_id', 'min']
    movies = pd.read_csv('..\\data\\filtered_responses.csv', sep=',', error_bad_lines=False, encoding="latin-1")
    movies.columns = ['movie_id', 'adult', 'type', 'max_min', 'global_rate', 'languages']
    new = pd.merge(history, movies, on='movie_id')
    new = new.drop(['adult', 'type', 'languages', 'global_rate'], axis=1)
    new['percentage'] = new.apply(column_switch, axis=1)
    new = new.drop(['max_min', 'min'], axis=1)
    new.head()
    reader = Reader(rating_scale=(0, 100))
    data2 = Dataset.load_from_df(new, reader)

    # Define a custom reader with the rating scale (usually from 1 to 5)
    reader = Reader(line_format='user item rating', sep=',', rating_scale=(1, 5))

    # Load the dataset using Surprise
    return Dataset.load_from_df(ratings, reader=reader), users, data2, users_ratings, movies


def train():
    # Load your dataset (assuming it's in a CSV format with columns: userId, movieId, rating)
    # Adjust the file path accordingly.
    file_path = '..\\data\\cleaned_rating.csv'

    # Load the dataset using Surprise
    data, users, data2, users_ratings, movies = load_data(file_path)

    # Split the dataset into a train set and a test set
    train_set, test_set = train_test_split(data, test_size=0.2, random_state=42)

    # Define the collaborative filtering algorithm (e.g., KNNBasic)
    sim_options = {
        'name': 'cosine',
        'user_based': True  # User-based collaborative filtering
    }
    model = KNNBasic(sim_options=sim_options)

    # Train the model on the training data
    model.fit(train_set)

    # Make predictions on the test set
    predictions = model.test(test_set)

    # Evaluate the model's performance using RMSE (Root Mean Squared Error)
    rmse = accuracy.rmse(predictions)
    print(f'RMSE: {rmse:.2f}')

    print(train_set.global_mean)

    # Now, you can use the trained model to make recommendations for a specific user
    user_id = '143079'  # Replace with the desired user ID
    user_ratings = np.array(list(map(lambda x: x[1], filter(lambda x: x[0] == user_id, data.raw_ratings))))

    # Get movie recommendations for the user
    movie_recommendations = []
    for movie_id in list(set(map(lambda x: x[1], data.raw_ratings))):
        if movie_id not in user_ratings:
            predictions = model.predict(user_id, movie_id)
            movie_entry = movies.loc[movies['movie_id'] == movie_id]
            if True in movie_entry['adult'].values:
                movie_recommendations.append((movie_id, 0))
            else:
                if predictions.details['was_impossible']:
                    global_rate = movie_entry['global_rate'].values
                    if len(global_rate) == 0:
                        global_rate = model.default_prediction()
                    else:
                        global_rate = global_rate[0]
                    user_row = users.loc[users['user_id'] == int(user_id)]
                    user_gender = user_row['gender'].values[0]
                    users_same_movie = users_ratings.loc[users_ratings['movie_id'] == movie_id]
                    users_same_gender = users_same_movie.loc[users_same_movie['gender'] == user_gender]
                    if len(users_same_gender) == 0:
                        movie_recommendations.append((movie_id, (global_rate / 10) * 5))
                    else:
                        predicted_rating = ((global_rate / 10) * 5 + users_same_gender.mean(axis=0, numeric_only=True)[
                            'rate']) / 2
                        movie_recommendations.append((movie_id, predicted_rating))
                else:
                    predicted_rating = predictions.est
                    movie_recommendations.append((movie_id, predicted_rating))

    # Sort the recommendations by predicted rating in descending order
    movie_recommendations.sort(key=lambda x: x[1], reverse=True)

    # Get the top N movie recommendations
    top_n = 20  # Replace with the desired number of recommendations
    top_movie_recommendations = movie_recommendations[:top_n]

    # Print the top recommendations
    print(f'Top {top_n} Movie Recommendations for User {user_id}:')
    for movie_id, predicted_rating in top_movie_recommendations:
        print(f'Movie ID: {movie_id}, Predicted Rating: {predicted_rating:.2f}')


if __name__ == '__main__':
    train()

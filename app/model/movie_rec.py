from surprise import Dataset, Reader
from surprise.model_selection import train_test_split
from surprise import KNNBasic
from surprise import accuracy
import pandas as pd
import numpy as np
import pickle
import os


def column_switch(column):
    if column['max_min'] != 0:
        return (column['min'] * 100) // column['max_min']
    return 0


def load_data(folder_path, rate_based):
    """
    Load the data and prepare them for the training.

    :param folder_path: The path of the folder containing all the csv files with the data.
    :param rate_based: If the collaborative filtering is based on the rates given by the users. If it is not based
    on the rates then it is based on the percentage of the movie seen by the user.
    :return: the dataset for the collaborative filtering, the database of the users, the database with the user and the
    ratings, and the database with the movies.
    """

    # Load the users database
    users = pd.read_csv(os.path.join(folder_path, 'user_data.csv'),
                        sep=',', on_bad_lines='skip', encoding="latin-1")
    users.columns = ['user_id', 'age', 'occupation', 'gender']

    # Load the ratings database
    ratings = pd.read_csv(os.path.join(folder_path, 'cleaned_rating.csv'),
                          sep=',', on_bad_lines='skip', encoding="latin-1")
    ratings.columns = ['user_id', 'movie_id', 'rate']

    # Create a database with users and ratings
    users_ratings = pd.merge(ratings, users, on='user_id')

    # Load the watching history database
    history = pd.read_csv(os.path.join(folder_path, 'movie_cleaned_1.csv'),
                          sep=',', on_bad_lines='skip', encoding="latin-1")
    history.columns = ['user_id', 'movie_id', 'min']

    # Load the movies database
    movies = pd.read_csv(os.path.join(folder_path, 'filtered_responses.csv'),
                         sep=',', on_bad_lines='skip', encoding="latin-1")
    movies.columns = ['movie_id', 'adult', 'type',
                      'max_min', 'global_rate', 'languages']

    # Create a database with the watching history and the percentage of the movie seen
    history_percentage = pd.merge(history, movies, on='movie_id')
    history_percentage = history_percentage.drop(
        ['adult', 'type', 'languages', 'global_rate'], axis=1)
    history_percentage['percentage'] = history_percentage.apply(
        column_switch, axis=1)
    history_percentage = history_percentage.drop(['max_min', 'min'], axis=1)
    history_percentage.head()

    # Create the Dataset for the collaborative filtering
    if rate_based:
        # Dataset based on the rates
        reader = Reader(line_format='user item rating',
                        sep=',', rating_scale=(1, 5))
        dataset = Dataset.load_from_df(ratings, reader=reader)
    else:
        # Dataset based on the percentages of the movie seen
        reader = Reader(rating_scale=(0, 100))
        dataset = Dataset.load_from_df(history_percentage, reader)

    return dataset, users, users_ratings, movies


def train_collaborative_filtering(train_set):
    """
    Train the model with the train dataset
    :return: the model
    """

    sim_options = {
        'name': 'cosine',  # Type of similarity function used
        'user_based': True  # User-based collaborative filtering
    }

    # Create the model
    model = KNNBasic(sim_options=sim_options)

    # Train the model on the training data
    model.fit(train_set)

    # save
    with open(os.path.join(os.path.normpath('/app'), 'model', 'model.pkl'), 'wb') as f:
        pickle.dump(model, f)

    return model


def test_collaborative_filtering(model, test_set):
    """
    Test of the collaborative filtering
    :param model: The model of the collaborative filtering
    :param test_set: The test dataset
    """

    # Make predictions on the test set
    predictions = model.test(test_set)

    # Evaluate the model's performance using RMSE (Root Mean Squared Error)
    accuracy.rmse(predictions)


def recommendation(user_id, nb_recommendation, dataset, movies, users, users_ratings):
    """
    Recommend a list of movies for a user based on collaborative filtering or demographic filtering when there are
    not enough data.

    :param user_id: The user id to make the prediction
    :param nb_recommendation: The number of recommendation asked
    :param dataset: The dataset used for train the model
    :param movies: All the movies
    :param users: All the users
    :param users_ratings: Database with the ratings and the users info
    :return: the recommendation
    :exception: The user have to exist in the database
    """

    # load the model
    with open(os.path.join(os.path.normpath('/app'), 'model', 'model.pkl'), 'rb') as f:
        model = pickle.load(f)

    # Get the array of the movies already rates by the user
    user_ratings_arr = np.array(list(map(lambda x: x[1], filter(
        lambda x: x[0] == user_id, dataset.raw_ratings))))

    # Get the array of all the movies
    movies_arr = np.array(list(set(map(lambda x: x[1], dataset.raw_ratings))))

    # Create an array with all the movies not seen yet by the user
    movies_not_seen = np.setdiff1d(movies_arr, user_ratings_arr)

    # Get the user entry in the database of all users
    user_row = users.loc[users['user_id'] == int(user_id)]
    assert len(user_row) > 0, 'The user does not exist in the users database'

    # Get the user gender ('F' or 'M')
    user_gender = user_row['gender'].values[0]

    # Get the user age
    user_age = user_row['age'].values[0]

    movie_recommendations = []
    for movie_id in movies_not_seen:

        # Get the movie entry in the database of all movies
        movie_entry = movies.loc[movies['movie_id'] == movie_id]

        # Filter to do not recommend adult movie to a kid
        if (True in movie_entry['adult'].values) and user_age < 18:
            movie_recommendations.append((movie_id, 0))
        else:
            # prediction of the collaborative filtering model
            prediction = model.predict(user_id, movie_id)

            # Test if the collaborative filtering prediction is not possible.
            # The prediction can be impossible if the user or the movie is new or have too few ratings (cold start)
            # If the prediction is not possible, do a demographic-based filtering.
            if prediction.details['was_impossible']:

                # Rate of the movie
                global_rate = movie_entry['global_rate'].values

                # If there are no global rate, give the default prediction
                if len(global_rate) == 0:
                    global_rate = model.default_prediction()
                else:
                    global_rate = global_rate[0]

                # Take all the ratings done by a user of the same gender
                users_same_movie = users_ratings.loc[users_ratings['movie_id'] == movie_id]
                users_same_gender = users_same_movie.loc[users_same_movie['gender'] == user_gender]

                # If at least one person of the same gender have rate the movie, consider it in the prediction
                if len(users_same_gender) == 0:
                    movie_recommendations.append(
                        (movie_id, (global_rate / 10) * 5))
                else:
                    predicted_rating = ((global_rate / 10) * 5 + users_same_gender.mean(axis=0, numeric_only=True)[
                        'rate']) / 2
                    movie_recommendations.append((movie_id, predicted_rating))
            else:
                # If the prediction is possible, use the collaborative filtering model
                predicted_rating = prediction.est
                movie_recommendations.append((movie_id, predicted_rating))

    # Sort the recommendations by predicted rating in descending order
    movie_recommendations.sort(key=lambda x: x[1], reverse=True)

    # Get the top N movie recommendations
    top_movie_recommendations = movie_recommendations[:nb_recommendation]

    return top_movie_recommendations


def print_recommendations(top_movie_recommendations, user_id):
    """
    Utility function to print the recommendation for a user.

    :param top_movie_recommendations: recommendations made by the recommender system
    :param user_id: The id of the user
    """

    print(
        f'Top {len(top_movie_recommendations)} Movie Recommendations for User {user_id}:')
    for movie_id, predicted_rating in top_movie_recommendations:
        print(
            f'Movie ID: {movie_id}, Predicted Rating: {predicted_rating:.2f}')


def train():
    # path where the data is
    file_path = os.path.join(os.path.normpath('/app'), 'data')

    # Load the dataset using Surprise
    dataset, users, users_ratings, movies = load_data(
        file_path, rate_based=True)

    # Split the dataset into a train set and a test set (20% test, 80% train)
    train_set, test_set = train_test_split(
        dataset, test_size=0.2, random_state=42)

    # Training
    model = train_collaborative_filtering(train_set)

    # Testing
    test_collaborative_filtering(model, test_set)


def get_recommendation(user_id):
    """
    Get the recommendation for a user

    :param user_id: the id of the user
    """
    # path where the data is
    file_path = os.path.join(os.path.normpath('/app'), 'data')

    # Load the dataset and databases
    dataset, users, users_ratings, movies = load_data(
        file_path, rate_based=True)

    # Get movie recommendations for a user
    nb_recommendation = 20
    recommendations = recommendation(
        user_id, nb_recommendation, dataset, movies, users, users_ratings)
    print_recommendations(recommendations, user_id)
    return [x[0] for x in recommendations]

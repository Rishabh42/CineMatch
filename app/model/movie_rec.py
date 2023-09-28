from surprise import Dataset, Reader
from surprise.model_selection import train_test_split
from surprise import KNNBasic
from surprise import accuracy

# Load your dataset (assuming it's in a CSV format with columns: userId, movieId, rating)
# Adjust the file path accordingly.
file_path = 'your_dataset.csv'

# Define a custom reader with the rating scale (usually from 1 to 5)
reader = Reader(line_format='user item rating', sep=',', rating_scale=(1, 5))

# Load the dataset using Surprise
data = Dataset.load_from_file(file_path, reader=reader)

# Split the dataset into a train set and a test set
trainset, testset = train_test_split(data, test_size=0.2, random_state=42)

# Define the collaborative filtering algorithm (e.g., KNNBasic)
sim_options = {
    'name': 'cosine',
    'user_based': True  # User-based collaborative filtering
}
model = KNNBasic(sim_options=sim_options)

# Train the model on the training data
model.fit(trainset)

# Make predictions on the test set
predictions = model.test(testset)

# Evaluate the model's performance using RMSE (Root Mean Squared Error)
rmse = accuracy.rmse(predictions)
print(f'RMSE: {rmse:.2f}')

# Now, you can use the trained model to make recommendations for a specific user
user_id = 'user123'  # Replace with the desired user ID
user_ratings = data.build_full_trainset().ur[user_id]  # Get the user's ratings

# Get movie recommendations for the user
movie_recommendations = []
for movie_id in data.build_full_trainset().all_items():
    if movie_id not in user_ratings:
        predicted_rating = model.predict(user_id, movie_id).est
        movie_recommendations.append((movie_id, predicted_rating))

# Sort the recommendations by predicted rating in descending order
movie_recommendations.sort(key=lambda x: x[1], reverse=True)

# Get the top N movie recommendations
top_n = 10  # Replace with the desired number of recommendations
top_movie_recommendations = movie_recommendations[:top_n]

# Print the top recommendations
print(f'Top {top_n} Movie Recommendations for User {user_id}:')
for movie_id, predicted_rating in top_movie_recommendations:
    print(f'Movie ID: {movie_id}, Predicted Rating: {predicted_rating:.2f}')

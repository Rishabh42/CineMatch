from flask import Flask
import requests
from model.movie_rec import get_recommendation, train, load_model
import os

app = Flask(__name__)

with app.app_context():
    # Train the model the first time the container is started and load it locally
    try:
        train()
    except Exception as exc:
        print(f"Error occurred while training model: {exc}")
    
    try:
        load_model()
    except Exception as exc:
        print(f"Error occurred while loading model: {exc}")


def get_user_details(userid):
    """
    Retrieve user details from the user API.

        :param userid: user id for prediction
    """
    try:
        response = requests.get(
            "http://fall2023-comp585.cs.mcgill.ca:8080/user/"+str(userid))
    except Exception as exc:
        print(f"Unexpected exception raised while getting user details: {exc}")
    
    if response.status_code != 200:
        return "Response not successful"
    
    return response.json()


def predict_movies(userid):
    """
    Return the list of movies from model's prediction

        :param userid: user id for prediction    
    """
    # we might have to send request to server to retrieve attributes for the user
    # these may be needed to send to the model.
    try:
        prediction = get_recommendation(userid)
    except Exception as exc:
        print(f"Unexpected exception raised while getting movie predictions: {exc}")

    return ",".join(prediction)


@app.route("/")
def welcome_return():
    return {"Welcome": "Hit the user ID end point - /recommend/<userid>"}


# define predict endpoint
@app.route('/recommend/<userid>')
def recommend_route(userid):
    return predict_movies(int(userid))


if __name__ == '__main__':
    app.run(port=8081)

# run the file using python3 app.py

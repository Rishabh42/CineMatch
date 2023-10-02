from flask import Flask
import requests
from model.movie_rec import get_recommendation, train
import os

app = Flask(__name__)

with app.app_context():
    # Check if a model is already present, if not train the model. This is to avoid training the model every time the container is restarted.
    print(os.environ.get('MODEL'))
    if os.environ.get('MODEL') != 'True':
        print("Training the model")
        train()
        os.environ['MODEL'] = 'True'
    else:
        print("Model trained already")


def get_user_details(userid):
    """
    Retrieve user details from the user API.

        :param userid: user id for prediction
    """
    response = requests.get(
        "http://fall2023-comp585.cs.mcgill.ca:8080/user/"+str(userid))
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

    prediction = get_recommendation(userid)
    return ",".join(prediction)


@app.route("/")
def welcome_return():
    return {"Welcome": "Hit the user ID end point - /recommend/<userid>"}


# define predict endpoint
@app.route('/recommend/<userid>')
def recommend_route(userid):
    return predict_movies(int(userid))


if __name__ == '__main__':
    app.run(port=8082)
# run the file using python3 app.py

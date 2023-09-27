from flask import Flask
import os
import pickle

app = Flask(__name__)

# dummy data
in_memory_datastore = {
   1: {"name": "COBOL", "publication_year": 1960, "contribution": "record data"},
   2: {"name": "ALGOL", "publication_year": 1958, "contribution": "scoping and nested functions"},
   3: {"name": "APL", "publication_year": 1962, "contribution": "array processing"},
   4: {"name": "BASIC", "publication_year": 1964, "contribution": "runtime interpretation, office tooling"}
}

# get the model loaded
MODEL_FILE = os.path.join("model", "classifier.pkl")
model = pickle.load(open(MODEL_FILE, "rb"))

# preprocessing of data
# retrieve the features for that particular user

def predict_movies(userid):
    # userid_load = userid
    # we might have to send request to server to retrieve attributes for the user
    # these may be needed to send to the model.
    return {userid:list(in_memory_datastore[userid].values())}

# define predict endpoint
@app.route('/recommend/<userid>')
def recommend_route(userid): 
    return predict_movies(int(userid))


if __name__ == "__main__":
    app.run(debug=True, port=8082)


# run the file using python3 app.py
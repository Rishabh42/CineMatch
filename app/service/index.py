from flask import Blueprint
import os
import pickle
import requests

service_api = Blueprint('service_api', __name__)

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

def get_user_details(userid):
    response = requests.get("http://fall2023-comp585.cs.mcgill.ca:8080/user/"+str(userid))
    if response.status_code != 200:
        return "Response not successful"
    return response.json()
 
def predict_movies(userid):
    # userid_load = userid
    # we might have to send request to server to retrieve attributes for the user
    # these may be needed to send to the model.
    print(get_user_details(userid)['age'])
    # return {userid:list(in_memory_datastore[userid].values())}
    output = ['toy+story+1995', 'toy+story+2+1999', 'toy+story+3+2010', 'toy+story+3+2010', 'toy+story+1995', 'toy+story+2+1999', 'toy+story+3+2010', 'toy+story+3+2010', 'toy+story+1995', 'toy+story+2+1999', 'toy+story+3+2010', 'toy+story+3+2010', 'toy+story+1995', 'toy+story+2+1999', 'toy+story+3+2010', 'toy+story+3+2010', 'toy+story+1995', 'toy+story+2+1999', 'toy+story+3+2010', 'toy+story+3+2010']
    return ",".join(output)


# define predict endpoint
@service_api.route('/<userid>')
def recommend_route(userid): 
    return predict_movies(int(userid))


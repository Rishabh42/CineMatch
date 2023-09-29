from flask import Flask
import os
from service.index import service_api

app = Flask(__name__)
app.register_blueprint(service_api, url_prefix='/recommend')


@app.route("/")
def welcome_return():
    return {"Welcome": "Hit the userID end point"}


if __name__ == "__main__":
    # Check if a model is already present, if not train the model. This is to avoid training the model every time the container is restarted.
    if os.environ.get('MODEL') != 'True':
        print("Train model")
        os.environ['MODEL'] = 'True'

    app.run(port=8082)


# run the file using python3 app.py

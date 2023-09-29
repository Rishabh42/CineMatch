from flask import Flask
from service.index import service_api

app = Flask(__name__)
app.register_blueprint(service_api, url_prefix = '/recommend')

@app.route("/")
def welcome_return():
    return {"Welcome": "hit the userID end point"}

if __name__ == "__main__":
    app.run(debug=True, port=8082)


# run the file using python3 app.py
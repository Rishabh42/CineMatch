import os
import sys
import subprocess
from emailer import send_email
from data_versioning import model_data_versioning

# Update the repo
subprocess.run(["git", "pull"])

sys.path.append("../")
# os.chdir('../')
from model.movie_rec import train
from model.movie_rec import test_collaborative_filtering
from data_processing_scripts.kafka_consumer_data_appender import run_kafka_consumer, run_processing_script, append_to_cleaned_data 

CURR = os.getcwd()
# print("---- CURR ----:",CURR)
# the current directory is the app directory

# Data collection & pre-processing
# TODO: use 15 minutes
run_kafka_consumer(1)
run_processing_script()
append_to_cleaned_data()

# train the model with new data
train(data_path=os.path.join(CURR, 'data'))
rmse_score = test_collaborative_filtering()

if rmse_score < 1:
    with open("auto_deployment/version.txt", "r") as f:
        version = f.read()
    next_version = str(int(version) + 1)

    # Write the updated version back to the file
    with open("auto_deployment/version.txt", "w") as f:
        f.write(next_version)

    subprocess.run(["dvc", "add", "model/model.pkl"])

    # Data versioning which can be offloaded to remote storage
    model_data_versioning(next_version,"./data", "./model")

    subprocess.run(["git", "add", "model/model.pkl.dvc", "model/.gitignore"])
    subprocess.run(["git", "add", "data/versioning", "model/versioning"])
    subprocess.run(["git", "add", "auto_deployment/version.txt"])
    subprocess.run(["git", "add", "data/cleaned_rating.csv"])
    subprocess.run(["git", "commit", "-m", "Data and Model version update: [" + next_version + "]"])
    subprocess.run(["git", "push"])

    # Success mail
    send_email("Successfully deployed new model","Your deployment of the new model was successful !")


else:
    # unsuccessful mail
    send_email(f"Deployment of new model failed","Deployment of new model failed since RMSE score of {rmse_score} is too high !")
    print(f"Deployment of new model failed since RMSE score of {rmse_score} is too high !")
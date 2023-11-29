import os
import sys
import subprocess
from emailer import send_email

# Update the repo
subprocess.run(["git", "pull"])

sys.path.append("../")
# os.chdir('../')
from model.movie_rec import train
from model.movie_rec import test_collaborative_filtering

CURR = os.getcwd()
# print("---- CURR ----:",CURR)

# TODO: Data collection script
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

    # TODO: Push the new cleaned_rating.csv instead of version.txt
    subprocess.run(["git", "add", "auto_deployment/version.txt"])
    subprocess.run(["git", "commit", "-m", "model version update" + next_version])
    subprocess.run(["git", "push"])

    # Success mail
    send_email("Successfully deployed new model","Your deployment of the new model was successful !")
else:
    # unsuccessful mail
    send_email(f"Deployment of new model failed","Deployment of new model failed since RMSE score of {rmse_score} is too high !")
    print(f"Deployment of new model failed since RMSE score of {rmse_score} is too high !")
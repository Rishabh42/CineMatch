import os
import sys
import subprocess

# Update the repo
subprocess.run(["git", "pull"])

sys.path.append("../")
from model.movie_rec import train
from model.movie_rec import test_collaborative_filtering

CURR = os.getcwd()
train(data_path=os.path.join(CURR, 'data'))
rmse_score = test_collaborative_filtering()

# TODO: Data collection script

if rmse_score < 1:
    # TODO: Success mail
    with open("auto_deployment/version.txt", "r") as f:
        version = f.read()
    next_version = str(int(version) + 1)

    # Write the updated version back to the file
    with open("auto_deployment/version.txt", "w") as f:
        f.write(next_version)

    subprocess.run(["git", "add", "auto_deployment/version.txt"])
    subprocess.run(["git", "commit", "-m", "model version update" + next_version])
    subprocess.run(["git", "push"])
else:
    # unsuccessful mail
    print(f"Deployment of new model failed since RMSE score of {rmse_score} is too high !")
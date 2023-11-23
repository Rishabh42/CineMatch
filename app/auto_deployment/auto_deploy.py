import os
import sys

sys.path.append("../")
from model.movie_rec import train
from model.movie_rec import test_collaborative_filtering

# os.chdir("../")
CURR = os.getcwd()
train(data_path=os.path.join(CURR, 'data'))
rmse_score = test_collaborative_filtering()

if rmse_score < 1:
    with open("auto_deployment/version.txt", "r") as f:
        version = f.read()
    next_version = str(int(version) + 1)
    print(next_version)

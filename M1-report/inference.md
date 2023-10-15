## **Inference service**

### Implementation of the recommendation service

The training weights were exported to the model file which can be used for making predictions in response to incoming requests from the simulator. We placed the model, app and its dependencies in a docker container which interfaces to port 8082 of the VM in McGill infrastructure.

### Design decisions

Since we did not want to retrain the model for each request, we are calling the training function when the docker container is started and it is mounted to persist across rebuilds. With the model loaded, we are calling the prediction on it after loading supporting data from the csv which is added in our container so that we do not have to query the simulator for user or movie attributes to provide as input to our model. To maintain the principle of separation of concerns, we kept the model and the prediction service in two distinct modules.

We wrapped the call to model in the prediction service and exposed it as the API endpoint for the get requests from the simulator. We would return the list of movies to the simulator. The list of movies is sorted by the rating score when provided to the prediction service as the output from the model.

### Architecture

The simulator hits the following endpoint 'recommend/<userid>' running on our team's machine (fall2023-comp585-4.cs.mcgill.ca) with 'GET' requests which then routes it to prediction service for handling. This was implemented in flask. To further reduce the load in terms of data loading on the container, we made a user_details fetcher in the request handler which would send back a query to the simulator on the user_api to fetch attributes (age, occupation and gender). As we had already scrapped the whole user data set (1 million users) by the time we submitted M1, we did not end up using back_queries for now. The predictions are returned to the handler service from the model (model's working described in learning.md). We return the predicted list (which is already sorted based on the rating's ranking) as a string to the simulator for which we see the success response in the kafka logs. We found that a list object (or) dictionary object is not interpreted as a successful response by the simulator.

### Load and infrastructure considerations

We deliberated on the following system design related issues which may arise due to scaling the requests. For instance, a load balancer could be exposed to the simulator API consisting of a buffer which will redirect the requests to multiple containers. Each container will consist of the model prediction service. Further, a performance argument could be made against the redundancy of maintaining multiple copies of the same model across different containers to ensure load balancing. This could be problematic while incorporating model updates and testing different model versions. Lastly, if we have huge datasets to be used for training, deploying the same datasets on multiple containers to train multiple models for load sharing can be further optimized. A fine tuned approach could be to split the dataset across containers so that training is distributed and we can combine the weights in a single container to form the model which can live on a separate container. We can use caching to serve the model weights or apply concepts similar to Content Delivery Networks to ensure fast servicing of prediction requests from multiple containers to which our load balancer is redirecting the requests. It is to be noted that we did not implement their resolutions considering the deadline for M1.

*Links to commits for the same*:

Integrate the inference service ([link](https://gitlab.cs.mcgill.ca/comp585_2023f/team-4/-/commit/4566105d1b007a154147004449541d5556f993f8))

Add inference support ([link](https://gitlab.cs.mcgill.ca/comp585_2023f/team-4/-/commit/cfa7f18d6e6ba5d7872e1677ead0d4b766e27775))

Refactor flask service ([link](https://gitlab.cs.mcgill.ca/comp585_2023f/team-4/-/commit/17f5d3d221c67758164ed2ad8d9b248f94675473))


### Dockerization of our inference service

We have placed the model file and the app driver code in the same container. Port (8082) inside the container is mapped to the port (8082) of the host machine (fall2023-comp585-4.cs.mcgill.ca) such that the requests received at the VM are forwarded to container's port when the container is deployed. We tried using the alpine version of the Python image to keep our container lightweight, but we found that packages end up with dependency errors. So we decided to use the Python base image (though larger) for the moment due to time constraints. We will work on optimizing the Docker container in the future. We set the working directory as app (base directory) in the container where we place the model and data directories. When we launch the container, we run the app.py to start our inference service. When started for the first time, we launch the training on the container for model creation to avoid packaging the model (2GB in size) within the containers as it would slow down the deployment.

### CI/CD pipeline

Though not part of milestone 1, we decided to leverage GitLab's CI/CD capabilities to set up a pipeline in the early stages of development. This is an important step in automating the development lifecycle. A pipeline was set up to automatically deploy the inference service onto a Docker container running on our remote server whenever code is merged into the main branch. A GitLab runner was set up on one of our teammate's local machine in order to run the CI/CD jobs. The CI/CD job itself used an Ubuntu Docker container to SSH into our remote server using a private key generated on the server. The private key was converted to base64 format and added as a masked GitLab CI/CD variable, which means that the variable is hidden in job logs. This is vital from a security standpoint. The job pulls the latest code from the GitLab repository, builds the Docker image and deploys the container. The CI/CD pipeline simplifies the process of deployment, precluding the need for manual intervention during the deployment stage.

*Links to commits for the same:*

Docker setup ([link](https://gitlab.cs.mcgill.ca/comp585_2023f/team-4/-/commit/fdf0481ed0bbdb3ed729a817ced950fc713c5047))

CI/CD setup ([link](https://gitlab.cs.mcgill.ca/comp585_2023f/team-4/-/commit/8fbe0ff3d371123cc565c335b7cb49c1c6261d50))

Testing CI/CD ([link](https://gitlab.cs.mcgill.ca/comp585_2023f/team-4/-/commit/834d7ceebe31e7827d5e573c85afdf30ede0f758))
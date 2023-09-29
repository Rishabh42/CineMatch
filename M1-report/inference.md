Inference service (1 page max): Briefly describe how you implemented the recommendation service. Provide a pointer to your implementation (e.g. to GitLab or other services).

### Implementation of the recommendation service
The training weights were exported to the model file which can be used for making predictions in response to incoming requests from the simulator. We placed the model, app and its dependencies in a docker container which is interfaces to port 8082 of the VM in McGill infrastructure.

#### Design decisions
did not want to retrain model for each request
wanted to keep the model part separate
wrap it in a prediction service which is exposed as an API end point

#### Architecture


#### Load and infrastructure considerations


#### How are containers made?


#### How are they shipped? We incorporated CI/CD


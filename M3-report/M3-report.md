# Milestone 3

## Containerization
We have four running containers for our inference service at all times: two containers for the stable deployment, one for the canary deployment and one for the load balancer. We additionally have containers running Prometheus and cadvisor as part of our monitoring service.

### Container set up 
#### Flask application
The containers for the stable and canary deployment of our application are built using the [same Dockerfile](/app/Dockerfile) with configurable options. They use a lightweight Python alpine image as the base image to minimize the size of the resulting image. Extra system dependencies needed to run the `surprise` library [^surp] for our recommendation service are installed onto the base image. Our container set up packs both the model and the inference service within the same container. Gunicorn is the web server used to deploy the Flask application. Gunicorn is a Python WSGI HTTP server ideal for deploying Python web applications in production [^gu].

#### Load balancer
We use NGINX as our load balancer [^nginx] to distribute the load between the stable and canary deployments. We again use an alpine version of the NGINX image to reduce the container size. Our custom [NGINX configuration](/app/nginx/nginx.conf) is mounted as a volume onto the container. 

### Orchestration and automatic container creation in CI/CD pipeline
We use [docker compose](/app/docker-compose.yml) to orchestrate the deployment of our containers. For the initial launch, all our containers can be created simply by running a single command in the `app` directory: `docker compose up -d`. During subsequent launches, a [bash script](/scripts/deploy.sh) in our CI/CD pipeline handles the creation and replacement of containers. Docker compose is used to take down or relaunch the required services. Containers are automatically created as part of our canary release pipeline. This process is explained in detail in the Releases section.

[^nginx]: https://www.nginx.com/
[^surp]: https://surpriselib.com/
[^gu]: https://gunicorn.org/ 

## Automated model updates
We implemented the automatic training and deployment of the models by developing a python script (`auto_deployment/auto_deploy.py`) which broadly performs the following tasks: \
\
**1. Data collection and pre-processing from the Kafka stream:** \
The raw data is collected from the Kafka stream for 15 minutes and pre-processed. After this it is appended to the records previously collected in `data/clean_rating.csv`.

**2. Training the models with the new data:** \
The newly collected data is now used to train the model \

**3. Checking if RMSE score is < 1:** \
We do our offline evaluation i.e. checking if RMSE score is less than 1  after the model has successfully been trained as described previously. If this condition is not satisfied, the new model doesn’t get deployed and the user gets an email mentioning that the new model wasn’t deployed and also reports the RMSE score.

**4. Versions the new model using DVC:** \
If the offline evaluation metric is satisfied, the new model gets versioned by DVC.

**5. Pushes the newly collected data to GitLab:** \
Finally, if everything works fine till this point, the newly collected data as well as the version is pushed to GitLab. This triggers the automated testing pipeline and also deploys the new model. 

**6. Users get notified via an email:** \
After the successful deployment of the model the users get an automated email confirming that the deployment was successful.

Additionally, we developed a Python scheduler script (`auto_deployment/scheduler.py`) which runs in the background on our team-4 server and triggers the auto deployment pipeline every 2 days.

**Links to the scripts involved:**
- Auto deployment script: https://gitlab.cs.mcgill.ca/comp585_2023f/team-4/-/blob/main/app/auto_deployment/auto_deploy.py 
- Scheduler: https://gitlab.cs.mcgill.ca/comp585_2023f/team-4/-/blob/main/app/auto_deployment/scheduler.py 


## Releases

### Triggering releases
As described in the previous section, when the new data is periodically pushed to our GitLab repository, the pipeline is triggered which passes through data quality checks ([test-data](/.gitlab-ci.yml)) and tests for the model ([test-model](/.gitlab-ci.yml)) and inference service ([test-app](/.gitlab-ci.yml)). If the tests run successfully, the final job of the pipeline `deploy` establishes an SSH connection to our server and pulls the latest version of our repository on the server. It then launches a [background script](/scripts/deploy.sh) to perform the canary release.

### Monitoring the release
The release script performs the following actions: (1) It kills the current canary container, builds a new image containing the new model and recreates the canary container. (2) It waits for 12 hours to allow the new deployment to stabilize and receive a fair amount of requests (3) After 12 hours, it sends a curl request to the Prometheus HTTP API to fetch the average response time of the successful requests over the past 12 hours. (4) Our threshold response time is 500ms. If the average response time is below the threshold, it builds a new image with the `stable` tag and recreates the two stable containers. At this point our canary release is successfully completed. If the average response time is greater than the threshold, the canary release is aborted by removing the canary container and sending an email notification to our team informing of the failed release.

### Load balancing
Our NGINX load balancer is configured to execute a 80-20 split of the incoming traffic between the two containers of the stable deployment and the canary container respectively. 

```
upstream backend {
        server inference_stable:5000 weight=4;
        server inference_canary:5001 weight=1;
    }
```

NGINX automatically distributes the load to available services in case any service is unavailable. For instance, when the canary container is recreated to deploy a new model, all traffic will be routed to the stable service when the container is being created. Similarly, all traffic will be momentarily directed to the canary container when the stable containers are being recreated to finish the new release. In any case, the downtime while recreating the containers is negligible, however, our load balancer ensures that we have zero downtime.

![Pipeline for canary release](/M3-report/artifacts/canary.png)
Figure 1: Workflow of canary release

### Metrics
Prometheus was set up to track metrics for our Flask application using `prometheus-flask-exporter` [^pfe]. This is a Python package that needs to be installed in our Flask application (check [app.py](/app/app.py)). It exports some default metrics like the response time for each request and the number of successful and failed requests.

```
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)
metrics = PrometheusMetrics(app)
```
To determine whether to perform the canary release, we perform the following PromQL query which computes the average of all recommendation requests. `flask_http_request_duration_seconds_sum` is a metric that gives the time taken for each request in seconds and `lask_http_request_duration_seconds_count` records the number of requests received.

`sum(flask_http_request_duration_seconds_sum{path=~"/recommend/.*"}) / sum(flask_http_request_duration_seconds_count{path=~"/recommend/.*"})`

[^pfe]: https://pypi.org/project/prometheus-flask-exporter/

### Provenance
Our idea behind having provenance in the system was to bind the data and models to our gitlab commits. We wanted to include precise commit messages to help us track the evolution of data/ model with each iteration. As the pipeline code is already tracked based on the commits, we figured this would be a good idea. It is to be noted that uploading models to gitlab is impractical due to size issues. Also, our deployment works through the code changes on our repo and it is heavily making use of gitlab CI/CD so we wanted the benefits of versioning using gitlab for models as well.

**We do the following:** On the host machine (our team-4 server), we have initialized dvc in the deployed github repo. We use it to create .dvc files for models. These files are metadata for the models which can be uploaded to gitlab for each version of the model. They primarily consist of md5 hash and as such are pretty small. the benefit is .dvc files provide a way for us to link models to commits without actually committing the big model files. We decided it would be the most practical to add the model file for tracking when data collection was happening. So whenever, our automated data collection script appends processed data to existing one on the host machine (outside of any container), we also initiate training of the model and include the resulting .dvc file of the tracked and trained model to the github commit. (**link to code demontrating that:** dvc tracking within automated data creation pipeline) It can be argued that the host machine does not possess resources to store different versions of model which is true as each model is roughly 2GB in size. We can offload those models to remote storage using dvc with the .dvc files acting as symbolic links. Since we did not have access to such a free remote storage to host multiple models, as a proof of concept: we kept different versions of models but in the form of .dvc files along with the data files. We committed these to the gitlab repo as well. This is to denote the remote offloading in real scenario. (**link to code demontrating that**: remote offloading and versioning)

This allows us to have a great versioning track record of the models and data. (**link to depict what I mean**)

**Further enhancement**: With the above approach, we were able to track the evolution of data and models along with the pipeline code but linking each individual recommendation with the pipeline code, model and data used to make that recommendation was difficult. We worked out the following approach:
- We created a new mysql container which would host a database on our team's server host machine. To put in perspective, this will be a separate container apart from the release containers and the host machine itself where the auto-data collection scripts were scheduled with cron job. Now the mysql container is having a persistently mounted storage. The mysql container is connected to the same docker network as the release containers and is part of docker compose.yml for releases. This was necessary to ensure database connection from within release containers to the mysql docker container. (**link to code implementation**: docker compose file)
- We created two tables in the database namely:
  - reccom (version_number INT, user_id INT);
  - tracking (version_number INT, data_creation TIMESTAMP, trained_on TIMESTAMP, model_rmse FLOAT);
- Since the mysql container had its port exposed, the host machine could insert data in the tracking table while the release containers were bound to the mysql database when the app was launched. The connection was opened and close using app_context and tear_down methods of flask. The release containers would insert records in reccom table linking version_number and user_ids of the recommendations being served.
- Lastly, with each iteration of data training and model updation: we increment a unique identifier in our auto_deployment module known as version_number which essentially tracks and relates the changes in data to models. It is to be noted that the version.txt file having the number is part of our commit whenever automated data updation happens. Now, each container would have its own copy of the version number depending on which model it is serving which in turn is dependent on the data being used to train it.
- As a result, we store the version_number, and the userID served by the container running that version of model+data along with the data creation timestamp, model creation timestamp and model_rmse score for that version_number in our database. Using a join query helps deliver the output of granular provenance per userID request. (**link to concrete example**: *we recorded a small video depicting it in action and explaining more*)
**example:** Following screenshot depicts the last two rows of the result set sorted in descending order for user_ids. We could not display all the rows due to space limitations in the screenshot.


link to mysql insertion query updates from container image:
  - helper functions:
link to host insertion queries:
  - helper functions:



**Reflection on Recommendation Service**
**Telemetry Collection System**
**Challenge:**

The initial challenge was managing a vast volume of logs. Loki was chosen for its promise of efficient storage, but it presented limitations in log retrieval and high CPU usage.


**Current Solution:**

Our team transitioned to a file-based system, opting to store logs in CSV files. This approach, while simpler, demanded more storage and necessitated regular log cleanups.


**Future Direction:**

With additional resources, the ideal solution would be to implement a database specifically for telemetry post-processing, aiming to enhance storage efficiency and retrieval capabilities.


**Load Balancing and Kubernetes**


**Challenge:**

Implementing Kubernetes for load balancing and canary deployment was challenging, particularly due to the lack of root access and difficulties in configuring load balancers on specific ports.


**Current Solution:**

Our team reverted to a simpler solution using an NGINX load balancer and bash scripts for canary deployment.


**Reflection:**

This part of the project highlighted the importance of balancing ambitious technological implementations with practical project management considerations.
Training Data for the Model


**Challenge:**

A critical aspect was the training data for the model. Our team faced the challenge of insufficient data, which limited the model's effectiveness and accuracy.


**Future Improvement:**

Moving forward, the focus will be on enhancing data collection and curation processes. Acquiring more comprehensive and diverse datasets is a primary goal to improve the model's performance and reliability.

### Contributions by Yaoqiang
**Data processing scripts for automated model updates**:

I worked on the Auto Development for M3. One of the significant contributions is which I implemented a script, kafka_consumer_data_appender.py, that streamlined our data handling. This script automates the collection and processing of real-time movie ratings from a Kafka server, elegantly solving the challenge of efficiently managing and integrating large data streams. 


Relevant commits:  

https://gitlab.cs.mcgill.ca/comp585_2023f/team-4/-/merge_requests/54/diffs?commit_id=480f1c1dd015bf125a39575ccd2f74802e74d1f8
https://gitlab.cs.mcgill.ca/comp585_2023f/team-4/-/merge_requests/54/diffs?commit_id=66c0123af5dd8c157352d673bcad5b94c064b6a9
https://gitlab.cs.mcgill.ca/comp585_2023f/team-4/-/merge_requests/55/diffs?commit_id=cd2667c60a08a0f9e2fc3051d39114a648ea7178
https://gitlab.cs.mcgill.ca/comp585_2023f/team-4/-/merge_requests/55/diffs?commit_id=ecbc4098be32718effc3d9b923460eea6ac18da1
https://gitlab.cs.mcgill.ca/comp585_2023f/team-4/-/merge_requests/55/diffs?commit_id=9672fb95d85d4137e965f7ea5442eb415558cf79

**Meeting management:**
led meetings on fairness analysis approaches and documented these sessions, providing clear and concise meeting notes for team reference.

Relevant commits:  
**Meeting notes created:**
https://gitlab.cs.mcgill.ca/comp585_2023f/team-4/-/merge_requests/54/diffs?commit_id=1c4f40512a48d7ae3a12f005c10ebd481bb7a1f9

**Pull requests reviewed by Yaoqiang:**  

https://gitlab.cs.mcgill.ca/comp585_2023f/team-4/-/merge_requests/52
https://gitlab.cs.mcgill.ca/comp585_2023f/team-4/-/merge_requests/51

**Report writing:**

https://gitlab.cs.mcgill.ca/comp585_2023f/team-4/-/commit/6e72b5ae933a3ea170835f9064b5134533d4b6f2

- Also brainstormed on the Auto Development with Rishabh.

### Contributions by Rishabh:
- **Developed the automated model updates script**  
(Corresponding issue: https://gitlab.cs.mcgill.ca/comp585_2023f/team-4/-/blob/main/app/auto_deployment/auto_deploy.py
- **Developed the Python scheduler:** https://gitlab.cs.mcgill.ca/comp585_2023f/team-4/-/blob/main/app/auto_deployment/scheduler.py 
- **Developed the email notification service:** https://gitlab.cs.mcgill.ca/comp585_2023f/team-4/-/blob/main/app/auto_deployment/emailer.py 
- **Pipeline/Offline eval metric** (Corresponding issue: https://gitlab.cs.mcgill.ca/comp585_2023f/team-4/-/issues/52) \
 **Code file:** https://gitlab.cs.mcgill.ca/comp585_2023f/team-4/-/blob/main/app/tests/model/test_model.py#L149 
- **Debugging and making sure that the pipeline is working fine**: https://gitlab.cs.mcgill.ca/comp585_2023f/team-4/-/issues/52 
- **Brainstormed with Varun on Canary releases, helped with the correct paths/routes and failing test cases.**
- **Assisted Yaoqiang with Kafka data processing**
- **Assisted Aayush with data integration in the `auto_deploy.py` script**
- **Repo quality assurance:** 
  1. Added rule to have at least 1 approval for MR 
  2. Added rule to merge only when the pipeline succeeds

**Merge requests reviewed by Rishabh:**
- Fixed the hanging bug: https://gitlab.cs.mcgill.ca/comp585_2023f/team-4/-/merge_requests/55
- Canary release set up and scripts: https://gitlab.cs.mcgill.ca/comp585_2023f/team-4/-/merge_requests/52
- Add the db provenance changes from data-integration to development: https://gitlab.cs.mcgill.ca/comp585_2023f/team-4/-/merge_requests/63
- Tamara fairness feedback loop: https://gitlab.cs.mcgill.ca/comp585_2023f/team-4/-/merge_requests/67

**Meeting notes created:** https://gitlab.cs.mcgill.ca/comp585_2023f/team-4/-/wikis/M3:-Issue-discussion,-debugging-and-development-sync-up


### Contributions by Aayush:
I have provided explanation on what I did and linked the commit for the same. The issue number is added in the commit message. Helps in linking issues to commit on gitlab.
- **Developed the dvc infrastructure - connected it auto data and model updates**: 
- **Set up the versioning for data files and models**:
- **Developed per request tracking solution** - Created the mysql container deployment, connected it with the auto updates, linked release containers to it so that insertion queries go through:
- **Fixed stale docker containers issue during data collection**:
- **Created slack and email alerts for failed canary containers deployment**: This is different from the pipeline canary failure mentioned above. This alert comes from the deploy script based on the average response time of the canary container:
- **Added the infrastructure for logging**:
- **Helped Rishabh with auto-deployment part**:

- I took initiative in the earlier part of the project to get things rolling because I had back to back exams and other deliverables near to M3 deadline. I raised this point with prof. too. As a result, I tended to ask everyone to stay back and meet after classes - get the momentum going.

- **Kubernetes**: I spent a lot of time trying to get kubernetes to run on our team's server. I worked closely on it with Varun and we spent around 4 days cumulatively. I learnt so much during the process but it led to a lot lost time which could have been used elsewhere. We were able to get it working only on port 80 of the exposed api which sadly was not practical for this project. The intention behind using kubernetes was the production grade capabilities for load balancing, canary releases and replicas to ensure availability. I even reached out to Deeksha for the same. I have extensively documented the issues observed and the command line remnants from one of the troubleshooting sessions.
link to issues in detail:
link to troubleshooting:
issues in short:

- Helping out the team with the general stuff: report writing, presentation, coordination and team management.

**Merge requests reviewed and raised:**


**Meeting notes created:**

note: I felt that everyone worked great for M3. Each member really got involved in the project and pushed as best as they could. I am quite pleased with how everyone collaborated and not just for the sake of points.
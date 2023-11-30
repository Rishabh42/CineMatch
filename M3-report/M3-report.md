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
(Corresponding issue: https://gitlab.cs.mcgill.ca/comp585_2023f/team-4/-/issues/58 ): https://gitlab.cs.mcgill.ca/comp585_2023f/team-4/-/blob/main/app/auto_deployment/auto_deploy.py 
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

**Merge requests reviewed:**
- Fixed the hanging bug: https://gitlab.cs.mcgill.ca/comp585_2023f/team-4/-/merge_requests/55
- Canary release set up and scripts: https://gitlab.cs.mcgill.ca/comp585_2023f/team-4/-/merge_requests/52

**Meeting notes created:** https://gitlab.cs.mcgill.ca/comp585_2023f/team-4/-/wikis/M3:-Issue-discussion,-debugging-and-development-sync-up

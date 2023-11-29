# Milestone 3

## Containerization
We have four running containers at all times: two containers for the stable deployment, one for the canary deployment and one for the load balancer. 

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

## Releases

As described in the previous section, when the new data is pushed to our GitLab repository, 
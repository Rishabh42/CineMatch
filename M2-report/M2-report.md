## Online evaluation

### Telemetry collection system
Our team initially considered the use of a standard database along with Python scripts to collect, process and store data from the Kafka stream in different formats. However, while exploring tools for our monitoring infrastructure, we came across Grafana Loki, an efficient log aggregation system inspired by Prometheus. Quoting from their description, "It is designed to be very cost effective and easy to operate. It does not index the contents of the logs, but rather a set of labels for each log stream." [^1] Considering the volume of data and the experiences of our peers shared during the M1 presentation, we decided to use Loki as our logs database. Loki seemed promising as it would help us evade both the problem of quickly running out space on our server with a local database or running out of limited free storage on a cloud database. We used the default Loki storage option, where logs are compressed and stored in chunks in the file system. The logs are rotated weekly. 

To send the logs from our Kafka stream to Grafana Loki, we used the agent Promtail. We also parsed and processed the logs with the help of Promtail. We defined four categories of logs: recommendation (successful recommendation requests with status 200), error (failed recommendation requests with status 0), history (records of the users' watch history, i.e. the GET /data endpoint) and rating (records of users' ratings for different movies, i.e. the GET /rate endpoint). Each log line was matched to a regular expression to identify its category. Named groups pertaining to important details were extracted from the log line and processed to create the final log to be sent to Loki in different formats depending on the category. (For example, *timestamp, userid, movied, minute_watched* for history and *timestamp, userid, error, error_msg, response_time* for error). An example can be found [here](http://fall2023-comp585-4.cs.mcgill.ca:3000/d/ce43d1d7-0e50-4bd0-95b8-3f28d8f9f804/monitoring-dashboard?orgId=1). This categorization of logs made it easy for us to fetch only the logs of interest during online evaluation and monitoring.   

[^1]: https://grafana.com/oss/loki/

## Monitoring

Our monitoring system operates on four main components: the telemetry collection system (described in the online evaluation section), the system metrics collection stack involving Prometheus, cAdvisor and node-exporter, the Grafana dashboard and the alert manager ([Docker configuration](https://gitlab.cs.mcgill.ca/comp585_2023f/team-4/-/blob/development/monitoring/docker-compose.yml))

### Prometheus
Prometheus was set up along with cAdvisor and node-exporter to scrape metrics from our running containers, such as resource usage, filesystem usage etc. In addition, Prometheus was configured to scrape metrics from Loki and Promtail as well. Custom metrics were defined in Promtail to collect the number of successful and failed recommendation requests, and a histogram of response time. 

### Grafana
Two dashboards were created in Grafana: the Logs dashboard ([link](http://fall2023-comp585-4.cs.mcgill.ca:3000/d/e027f147-6f47-4cf3-b7af-8ffa87ac664b/logs-dashboard?orgId=1)) and the Monitoring dashboard ([link](http://fall2023-comp585-4.cs.mcgill.ca:3000/d/ce43d1d7-0e50-4bd0-95b8-3f28d8f9f804/monitoring-dashboard?orgId=1)). The Logs dashboard provides a playground to view and explore the 4 categories of logs collected by Loki, as explained in the online evaluation section. 
![logs_dashboard](/M2-report/artifacts/logs.png)

The Monitoring dashboard is made up of two parts. The first row provides visualizations and statistics to monitor the availability of our recommendation system. In particular, it display the number of successful and timed out requests obtained from the custom Promtail metrics, along with the percentage of failed recommendations. There is a panel to monitor the health of our recommender service infrastructure, that displays the number of associated running containers. Our recommender service has 3 containers, one nginx load balancer and two instances of our Flask service. Thus, this metric should always have a value of 3. We also provide the CPU usage to monitor that our service is not overloaded. 
![availability](/M2-report/artifacts/availability.png)

The second row monitors the model quality. Currently, we have two plots derived from the histogram metric: the average response time and the a histogram of the response time. The histogram gives us a picture of the distribution of the response time.
![model_quality](/M2-report/artifacts/model_quality.png)

### Alert Manager
Three rules were defined in Prometheus to trigger alerts in case of aberrations in the running of the recommendation service.
Alert Manager was set up to send the alerts on our private group channel on the COMP585_ISS_A2023 Slack server. ([rules.yml](../monitoring/prometheus/rules.yml))
- Alert when any of the services Prometheus is monitoring is down for more than 2 minutes (cadvisor, node-exporter, promtail, loki). This rule was set up to ensure that the monitoring infrastructure itself is functioning well
- Alert when any one of the three recommendation service containers (1 nginx and 2 flask) goes down. This rule is very important as this alert could imply that there is a disruption in our service or that the server would get overloaded (with just one flask container running)
- Alert when more than 80% of recommendation requests time out. This rule is important as it means that our service is largely unavailable and requires immediate diagnosis. 

![Slack alert](/M2-report/artifacts/slack.png)

## Individual Contributions and Meeting Notes

Varun:
- Telemetry collection with Grafana Loki for online evaluation and monitoring ([aadc2c404585065281e06a770d7b342a234126fb](https://gitlab.cs.mcgill.ca/comp585_2023f/team-4/-/commit/aadc2c404585065281e06a770d7b342a234126fb#8e05eaea18b007dfcb04181c00986195057b2bd5_41_27)), scripts for scraping([fe5d2c330ccd0eee67ebc83af93bf314ab18f80e](https://gitlab.cs.mcgill.ca/comp585_2023f/team-4/-/commit/fe5d2c330ccd0eee67ebc83af93bf314ab18f80e#4530003189c923e22abae61d6fa8e0b5450e12d9_6_26))
- Prometheus and metrics collector setup ([854e27821bd5acc5dc39c64db312a18d6fda2ed6](854e27821bd5acc5dc39c64db312a18d6fda2ed6))
- Grafana dashboard ([link](http://fall2023-comp585-4.cs.mcgill.ca:3000/d/ce43d1d7-0e50-4bd0-95b8-3f28d8f9f804/monitoring-dashboard?orgId=1), [link](http://fall2023-comp585-4.cs.mcgill.ca:3000/d/ce43d1d7-0e50-4bd0-95b8-3f28d8f9f804/monitoring-dashboard?orgId=1))
- Prometheus alert manager ([854e27821bd5acc5dc39c64db312a18d6fda2ed6](https://gitlab.cs.mcgill.ca/comp585_2023f/team-4/-/commit/854e27821bd5acc5dc39c64db312a18d6fda2ed6#a4708f6ad79a30d8c3e0b92167de3cd6af006082_0_1), [854e27821bd5acc5dc39c64db312a18d6fda2ed6](https://gitlab.cs.mcgill.ca/comp585_2023f/team-4/-/commit/854e27821bd5acc5dc39c64db312a18d6fda2ed6#97d836bf195b7e218fbd77fb28d17cad24eb05cb_0_1))
- Report for telemetry collection system and monitoring  ([252f6f3ab5177a5403bd0bd4d4c81c33369bd5c9](252f6f3ab5177a5403bd0bd4d4c81c33369bd5c9))
- Pull requests
    - Requested review: [!36](https://gitlab.cs.mcgill.ca/comp585_2023f/team-4/-/merge_requests/36)
    - Provided review: [!41](https://gitlab.cs.mcgill.ca/comp585_2023f/team-4/-/merge_requests/41#note_61552)
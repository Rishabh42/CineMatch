## Data Quality

### What makes data "high quality" in our context? 
_Common dimensions of data quality include accuracy, completeness, consistency, reliability, and timeliness._

Our pipeline for data was as follows:
- Save the logs to flat files.
- Preprocess the flat files to clean data collected. Inspection was done to identify any obvious issues with the data collected. We found missing values and spurious entries. We dropped all those records.
- Filter and segregate data collected according to the type of data files. Convert them to csv files.

- The user data was scrapped from the simulator API for 1 million users.
- Movie attributes were scrapped from the API for the items obtained from kafka logs.
    - As an enhancement, we loaded the movie attributes and imdb ratings from external sources too for M2. This was done using the "tmdb_id" attribute we had for each movie
    
    ### how can you use the external imdb files?

    The movieids from the simulator comprise of the name of the movie and the year separated by '+' symbol. Movie attributes returned by the simulator contain a mixture of data from imdb and tmdb datasets. There are unique ids corresponding to each of these datasets in the response. We want to use the imdb dataset as an external source and found that the name of the movie corresponds to original column of the imdb dataset and the year to endyear column. Through this we can obtain the imdb_id which can be used to join to other tables from imdb to get more information for the movies.


    - From the kafka logs, sometimes we would get made up movie details. Since it was mentioned in the requirements of the project that the simulator is using imdb movie database to generate logs, we went directly to the external source to avoid such spurious logs.

- Kafka logs are responsible for giving watch history, telemetry and ratings by each user (whether the liked the movie or not). We loaded the kafka logs to grafana monitoring. Further, we found that grafana can be used a database to serve the logs in response to API queries. So to retrieve real time information about the system for online evaluation, we added processing at the destination endpoint of those API queries to get filtered data outputs.

### Data processing at different end points
One notable aspect was the handling of data at end points. Since we have parsed logs to loki and were accessing them through grafana, we made sure to take care of duplicates and spurious values when retrieving data through those end points.

### Data quality reports
We generated reports for each of the data set used for training the model. In the report we tracked missing cells, duplicate rows, memory size, variable types, distinct values, data range and correlation among attributes. Following are the screenshots from one of our data reports:

![data_quality_1](/M2-report/artifacts/data_profile_1.PNG)
![data_quality_2](/M2-report/artifacts/data_profile_2.PNG)
![data_quality_3](/M2-report/artifacts/data_profile_3.PNG)
![data_quality_4](/M2-report/artifacts/data_profile_4.PNG)
![data_quality_5](/M2-report/artifacts/data_profile_5.PNG)

### Links to artifacts
[loki scrapper remove duplication at end point](https://gitlab.cs.mcgill.ca/comp585_2023f/team-4/-/commit/5c5e121b6102908d30678242ef0907681089fcb1#d2ceaa5dc9ddd0e2120592bc7329c5fff765d791_0_52)

[data processing scripts](https://gitlab.cs.mcgill.ca/comp585_2023f/team-4/-/tree/development/app/data_processing_scripts)

[end point data processing](https://gitlab.cs.mcgill.ca/comp585_2023f/team-4/-/commit/5c5e121b6102908d30678242ef0907681089fcb1#33c123951964e87db9810f2101b3da7faf79bdac_0_12)



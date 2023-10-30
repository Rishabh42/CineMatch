### Data processing tests
We added made sure to add tests while considering that we do not introduce test specific flows in the programs. The unit tests were added to run before the deployment pipeline so that regression tests were covered. For data preprocessing scripts, unit tests for fetching movies, filtering movies and sending curl requests to API for creating the dataset were covered. We also included negative cases and tests to unpack the ratings and history data. Dummy dataset files were used so that the unit tests do not have to interface with actual data and make these unit tests pretty quick. 

### Test reports and runners
Most of the unit tests were written in pytests. They were kept under tests directory on the app folder. Some tests had to be kept outside because of relative module import issues. We used html-report package added as a plugin to the pytest runner so that we can generate reports for our test suites. The report runner keeps track of the history of the past runs. It saved in the archival files which are read everytime report is generated.

Following are the artifacts from our test reports:
![test report 1](/M2-report/artifacts/test_report_1.PNG)
![test report 2](/M2-report/artifacts/test_report_2.PNG)
![test report 3](/M2-report/artifacts/test_report_3.PNG)
![test report 4](/M2-report/artifacts/test_report_4.PNG)

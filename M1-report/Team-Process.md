# Team Process and Meeting Notes

**Team Organization**:  
Our team was organized with an intention to contribute activly and equally. We set up the roles in our workflow (A0) and  assigned the team members based on individual strengths and experience, ranging from data engineering, backend development to machine learning. This effective categorization in roles helped us to better collaborate and ensuring project completion.

**Communication Channels**:  
Our team mostly used Slack and WhatsApp for day-to-day communication and updates. two weekly meetings were scheduled after classes, with both in-person and virtual Zoom sessions. To maintain documentation, GitLab was our platform of choice.

**Work Division & Responsibilities**:  
As from our meeting, the work was divided as:

Yaoqiang (Luke):  
Data Engineer responsible for data creation and preprocessing.

Tamara: 
ML Engineers in charge of implementing the machine learning model.

Rishabh:
ML Engineer in charge of implementing the machine learning model and collecting \& pre-processing the datasets

Aayush: 
Backend Engineer tasked with developing the inference service.

Varun: 
MLOps Engineer, overlooking deployment and CI/CD

Our meetings served as a platform to discuss progress, brainstorm ideas, set up ToDos, and divide work for the coming week. We made discussions on model type, data creation, and task distribution for a each weeks delivery and assiged the tasks to the corresponding team member. In terms of individual contributions, Luke took charge of dataset creation, while Tamara and Rishabh began implementing the ML models. Aayush dived deep into backend development, and Varun focused on deployment essentials.

**Links to our meeting notes**:
https://gitlab.cs.mcgill.ca/comp585_2023f/team-4/-/tree/development/meeting-notes

**Links to our team member commits**:

Data collection and preprocessing(Yaoqiang):  
https://gitlab.cs.mcgill.ca/comp585_2023f/team-4/-/commit/bf82820d1affab62a0677fb71e49774f738ef5f1

Varun:
Dockerfile setup: https://gitlab.cs.mcgill.ca/comp585_2023f/team-4/-/commit/fdf0481ed0bbdb3ed729a817ced950fc713c5047
CI/CD setup: https://gitlab.cs.mcgill.ca/comp585_2023f/team-4/-/commit/8fbe0ff3d371123cc565c335b7cb49c1c6261d50
Documentation: https://gitlab.cs.mcgill.ca/comp585_2023f/team-4/-/commit/79f5136fab86fcd14e0b49b9884c904052103170

Inference service(Aayush):  
Create inference service, help with deployment:
here ([link](https://gitlab.cs.mcgill.ca/comp585_2023f/team-4/-/commit/a8e3116e65c35ac300b9c40ed5238775ceed2223)) here ([link](https://gitlab.cs.mcgill.ca/comp585_2023f/team-4/-/commit/4566105d1b007a154147004449541d5556f993f8))  
Ratings and Users - fetch and dataset creation: here ([link](https://gitlab.cs.mcgill.ca/comp585_2023f/team-4/-/commit/6f6eda5706550a5b97f25ec4b8caab5df96e1756))  
Documentation and restructuring of code: here ([link](https://gitlab.cs.mcgill.ca/comp585_2023f/team-4/-/commit/17f5d3d221c67758164ed2ad8d9b248f94675473)) here ([link](https://gitlab.cs.mcgill.ca/comp585_2023f/team-4/-/commit/22f7bf9deca26b9caf8d7b401cfa47b84fc41809))

Model implementation(Tamara & Rishabh):

Rishabh:  
Collaborative filter model: https://gitlab.cs.mcgill.ca/comp585_2023f/team-4/-/commit/be9a020284ce5d361e44da83cbe26beeeab1bb62  
Data fetching and pre-processing scripts: https://gitlab.cs.mcgill.ca/comp585_2023f/team-4/-/commit/a4d64024d42ddc13dc4405cefc2d8e7458d40f30  
Compiled datasets: https://gitlab.cs.mcgill.ca/comp585_2023f/team-4/-/commit/b07ff1b98e6c50dfdd10cf72aa6850db6bdff545

Tamara:  
Collaborative filter: https://gitlab.cs.mcgill.ca/comp585_2023f/team-4/-/commit/d1f1596cb2e8ad67773bbbd1cc62f12afeadc956  
Other filters: https://gitlab.cs.mcgill.ca/comp585_2023f/team-4/-/commit/2da2427553fface20fc5ab54fd375ddecf4336fd  
Documentation, cleaning and re-structuration of the code: https://gitlab.cs.mcgill.ca/comp585_2023f/team-4/-/commit/f1c5309b01b8b125c9b4592423c64c742233b87e  

## Comparison to our original workflow  
Compared to the original workflow, every team member performed the allotted tasks on time and in a collaborative manner. Regular meetings were held amongst group members and the work was done smoothly.

**Frequency of meetings:**  
- Initially we planned on meeting once a week but as the development progressed we had to meet at least twice in a week as the deadline for M1 approached.
- Each team member was present in the meetings either virtually or in person

**What are the responsibilities of each team member during the meetings?**  
- We synced up on development, discussed any issues being faced by teammates and resolved them in each meeting. 
- Notes and meeting minutes were created by almost each team member in the meetings
- Overall, each team member delivered on their responsibilities 

**How will internal deadlines be set, managed, and followed?**  
- We used GitLab issues to assign tasks to each team member and used the `Due date` parameter to manage deadlines. Additionally we created labels for each functionality. 
- For some tasks like implementation of the model and dataset collection, it was taking some time in researching and coming up with the most optimal recommender approach to be used. During this time, one of our team members fell sick so we had to adjust the deadlines. In the end we were able to achieve the allotted tasks despite the unfortunate delay

**How will you coordinate your work?**  
- As explained above, we used GitLab for syncing the code, allotting tasks and managing deadlines.
- We also used our team server to share large files like the data files which were used in training the model

**What will be done in case disagreement arises?**  
Fortunately, we didn’t have any major disagreements since we communicated & collaborated effectively.

**Modes of communication?**  
We used the following modes of communication as was discussed in our original workflow:
- In person meetings
- GitLab issues for dividing work
- Slack and WhatsApp groups for easy communication
- Zoom meetings and voice calls

**Conclussion**:  
While our orignial workflow was mostly outlined in our initial workflow, a few adaptions were made in response to some challenges we faced. For instance, we initially underestimated the complexity of model deployment, leading us to revisit and refine our approach. Additionally, We had believed that the complexity of our data wouldn't necessarily to be a large dataset. However, as we delved deeper into the implementation phase, it became an evidence that It is important to get a larger dataset. So we spent a bit more time on collecting and generating the dataset.

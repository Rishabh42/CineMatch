# 1

# 1.1.
**Explain what kind of system you select in this assignment and the reasons for your selection. [5]**

After deliberating on a couple of potential ML enabled products, we picked notion for this assignment specifically their offering combining AI capabilities with the traditional note taking software in the form of notion AI. To provide a bit more context, notion possesses advanced capabilities in comparison to a traditional note taking app such as google keep or onenote. It combines into a single system the processes for taking notes on projects, knowledge management and collaboration. For a user who is a student or researcher, these capabilities can prove to be extremely useful.

We picked notion AI because we wanted to explore how AI may help to enhance user experience when the traditional deterministic notion app has been able to satisfy most of their users. It is a good opportunity to depict clearly how AI may be able to carve a niche for itself even in scenarios where usecases have been defined and satisfied unambiguously by existing apps.

A student or a full-time researcher (working within academia) would expect flexibility and customisation in their workspace for taking notes. They would want integrations with third parties and the ability to export their notes in an unrestricted manner. There should be support for figures, looks and media to be embedded with the notes. Further, it should be free or sufficiently cheap such that cost is not a barrier for these categories of users. Notion AI takes things a step further by providing:



* Intelligent search based on user intent and considers the context of the information provided to give output from existing notes and external data.
* It can suggest workflows to users providing task automation and save them time and effort.
* It provides insights on the existing notes the user has stored and offers a personalized experience to the users. Teams can facilitate collaboration by taking up the role of managing logistics for the team’s workspace.

## 1.2.

**Discuss what kind of problem the intelligent system is trying to solve. What makes this problem hard? What are the particular strengths of having an intelligent system rather than a traditional system with deterministic behavior? What are the weaknesses of an intelligent system in this context compared to a traditional system? [15]**

**Intended users:** We are considering the primary users as students actively involved in studying or learning. Further, researchers requiring a tool to support their day-to-day activities are also part of the primary user group considered. We expect that all the users will be accessing the app through commonly available devices (mobile/ pc) and they would want cross platform compatibility. We do not expect the users to spend a lot of time in setting up the app for their use nor do we expect them to be willing to invest large sums of money to streamline their note taking and knowledge sharing workflow. However, these users owing to the nature of their work - study and research then sharing their knowledge - will be quite demanding in terms of the features they would expect from the app. Lastly, if the app is intended to support their learning activities so if using the app proves too complicated or slow such that it hinders their studying then it will not be adopted by the user, no matter how superior the features being offered by the app are.

#### What kind of problem the intelligent system is trying to solve?

**Information overload:** Usually, the users will create notes for a host of topics across a variety of subjects. This process will go on usually for a whole term or a school year. In the case of research projects, it can be even longer. The students/ researchers do not have much time to organize, sort and categorize this exponentially growing amount of data. What ends up happening is at the end, there is a big notebook with disjointed notes spread here and there. The user may not always end up with the same organizing scheme for their notes with which they initially started. Notion AI can solve this problem by interpreting and organizing the large datasets created by the user. It offers information retrieval and intelligent search capabilities based on the user’s intent.

**Automation:** To support users and free up their time, notion AI can automate repetitive tasks which users perform while taking notes or managing their projects. This involves suggesting workflows to the users automating a sequence of actions based on the past usage patterns. For instance, it can create reminders for the team’s workspace, rephrase the meeting notes, make them longer or shorter and automatically check off items off the checklist when they get completed. This sort of logistical support can be quite beneficial to keep things in order for a student/ researcher who may not be willing to spend quite a bit of time on these things and lead to a boost in productivity.

**Collaboration:** Frequently, multiple students have to work together on a project or an assignment. Notion provides the capabilities to allow different team members to work together seamlessly. Notion AI goes further ahead and provides capabilities to brainstorm new ideas as a team, plan projects and highlight action items and key takeaways from the meetings. 

**Personalized for each user:** Elaborating on the above mentioned point, notion AI does all this while ensuring that needs of all its diverse users are met at a personalized level. It learns the usage pattern for each user and delivers a unique experience to each user based on what suits them best. Notion AI adds generatie AI capabilities while delivering a personalized user experience.

#### What makes this problem hard?

**Exponential growth of data:** The amount of data which the app has to deal with is tremendous. For instance, there will be notes created by the user. There will be usage data based on the tracked user behavior in the app. There will be data from external sources to create a LLM. On top of that, there needs to be a feedback loop in this system. There needs to be control on the type of data being ingested for ML training and the outputs being produced. The app should not carry forward bias from its training data. The data created by users (notes) needs to be encrypted. Now, further complexity will arise because all this data is being created very quickly.

**Distributed system challenges:** A major selling point of the app is the focus on ensuring high productivity and collaboration among members across different platforms. There is little scope for lags and downtime. Model deployment and training should happen without affecting existing infrastructure. User data needs to be kept safe and in sync across all devices at all times. This would require solving some complicated distributed system engineering challenges to handle the huge number of devices.

**Handling privacy concerns:** 

* The data created by users (notes) needs to be kept safe(encrypted) at all times on all devices regardless of which AI enabled feature is being added to the app. There should be a clear separation of concerns and no unnecessary decryption of the notes. The user data should not be moved to different servers unless it is absolutely essential.
* It is plausible that a lot of users may not want their personal notes to be used for training models. There can be different laws governing the use of data for model training in different geographies (GDPR in Europe), so the app should have an opt -out feature available for users in cases where they don’t want their data to be ingested by the models. Further, there should be a way to accommodate their requests should they change their minds in the future and choose not to include their data in the ML model. In that case, retraining the model without their data may prove to be too costly. 

**Personalized experiences with gen AI:**

Building on top of the previous point, when the app can indeed learn from the user’s notes data, offering them a personalized enough experience through notion AI will be challenging. This is because it may be easy to offer everyone similar experience which is personal superficially but to truly cater to their individual needs and anticipating it based on their usage patterns and notes without simply mirroring the trends learned from the aggregated data will be challenging. It is possible that an extremely good implementation of such a system may prove to be too eerie for some users (they may interpret it as quite unnatural as if someone is peering over their shoulders while they are working). Then, the next challenge will be to define how personal is too personal.

#### What are the particular strengths of having an intelligent system rather than a traditional system with deterministic behavior?

**Adaptable:** It will be extremely flexible for users unlike a traditional deterministic system. They will be able to extract themes from existing data, summarize texts, generate new ideas and improve their writing by rephrasing entire work. Students and researchers may find it quite useful to overcome writer’s block whale drafting reports. Since notion has a strong support for embedding external content along with the notes, notion AI will add the capability to manipulate the embedded content as well within the scope of the app.

**Handle ambiguity:** Sometimes, there are cases when the user is not sure about how best to convey what they want to do in the app. They might be going through iterations of building up the idea and may not directly arrive at the steps to be fed to a deterministic system. Notion AI will help users in working with them through these iterations. It offers a chat-like interface (similar to chatGPT) so that user can work together with the AI assistant to create their content.

**Enhanced user experience:**

Because the user need not mention all the steps explicitly nor do they need to write complete content, this reduces the effort required from the user to a large extent. No longer is the onus of creating the content solely on the user, but the notion AI will support the user through this process. This makes things easier for the user and the added features lead to an enhanced user experience.

**Efficiency and productivity:** With the help of the generative capabilities of the assistant, the user can offload some parts of the tasks for creating content and the admin tasks for managing notes entirely on the notion AI assistant. This will lead to greater productivity for the users as they can get more done in the same amount of time.

#### What are the weaknesses of an intelligent system in this context compared to a traditional system?

**Data training and aggregation:** As opposed to a traditional system, notion AI will require huge amounts of data for training. The aggregation of data was not required previously for deterministic systems. They were much more concerned about handling large amounts of data but that would come in the later stages of the product’s lifecycle. For intelligent systems, before they can be offered to the users, there needs to be a sizable chunk of training data so that the features being offered work as intended and do not end up giving gibberish as output. 

**Privacy concerns:** When the developers aggregate such huge amounts of data, there is bound to be privacy concerns because all of that data cannot be obtained in-house. They would have to go to external sources to retrieve the data but that part becomes increasingly murky in terms of how that data is collected at source. Further, the intelligent systems are effectively much more intrusive of the user’s privacy because in a way they have greater awareness of the user’s patterns. If the trained model is somehow hacked, then effectively the company has handed over patterns and nuances of a large number of users distilled and stored in a condensed manner, to the nefarious entities. 

**Infrastructure:** Creating the infrastructure to deploy, test and iteratively develop an intelligent system is much more complex than a traditional note taking app because on top of the features which are available in the deterministic app, the developers have to integrate generative AI features as well. To the user, it may appear as a single feature but behind the scenes, it will spawn a whole new section of the app owing to the data collection, training and deployment challenges associated with ML workloads. 

**Bias:** The models trained are only as good as the data provided to them. Since, the data will be ingested from a variety of sources, it will be the responsibility of the developers to ensure that the notion AI features does not end up generating content which is insensitive and harmful to its users and public at large as that can open the company to a lot of legal exposure.

**Interpretability:** To ensure accountability of its intelligent capabilities, having a system which can explain how and why certain decisions were made by the AI assistant can be very useful. If such a record can be maintained for each user along with the logs of the app, then it can be useful to troubleshoot issues in the intelligent system and not make it seem a black box like it is as of now. But implementing such a system is quite challenging and research is ongoing.

### References:

1. [Working as team with notion AI](https://www.notion.so/help/guides/how-product-teams-boost-productivity-and-spark-new-ideas-with-notion-ai)
2. [Notion-for-education](https://www.notion.so/product/notion-for-education)
3. User comment from reddit: [notion_ai_works_so_great](https://www.reddit.com/r/Notion/comments/10r8qwu/notion_ai_works_so_great/)
4. [whats_the_point_of_paying_10_monthly_for_notion](https://www.reddit.com/r/Notion/comments/11auryk/whats_the_point_of_paying_10_monthly_for_notion/)
5. User comment from reddit: [link](https://www.reddit.com/r/Notion/comments/12etz1i/not_sure_what_the_fuss_is_about_with_notion_ai/)
6. [ive_changed_my_mind_about_notion_ai](https://www.reddit.com/r/Notion/comments/12g6j3i/ive_changed_my_mind_about_notion_ai/)
7. [notion_ai_is_phenomenal](https://www.reddit.com/r/Notion/comments/12dfzu0/notion_ai_is_phenomenal/)
8. [notion-for-academic-research-management](https://andymcdonaldgeo.medium.com/notion-for-academic-research-management-9cb81a333d75)
9. [academic-research-notion](https://girlknowstech.com/academic-research-notion/)
10. Guide: [using-notion-ai](https://www.notion.so/help/guides/using-notion-ai)


#
## 2.1
#### User classes:
The different user classes of Notion, and how these different user classes use Notion:
- **Students**
	- Take lecture notes
	- Collaborate with other students on group projects
	- Keep track of their assignments and their progress in each classes
- **Team**
	- Collaborate on documents between team members
	- Take notes during meetings
	- Keep track of the project
	- Manage tasks of the team
- **Teachers or Professors**
	- Take notes for their classes, organize their course material
	- Keep track of their classes and progress of each student
	- Share resources with students
- **Company**
	- Quicky create shareable links from documents, for example to share a presentation of a project
	- Create documentation (for example, a hardware usage tutorial)
	- Manage projects by sharing notes, tasks, progress and documents amongst team members and with different teams.
- **Researchers**
	- Gather data
	- Organize research notes
	- Collaborate on research projects
- **Freelancers**
	- Keeping track of the progress of their projects
	- Manage their client projects
	- Maintain a portfolio
- **Artists, writer or content creator**
	- Noting new ideas and writing some drafts
	- The ease of use also helps them in not spending much time on the software so they can rather spend time on creative ideas and inspiration
	- Organize their projects

#### Other stakeholders:
The other stakeholders of Notion, and why they may have an interest in Notion:
- **Notion's partners**
	- Integrate Notion in their product
	- Provide a service to Notion
- **Notion's Investors or Owner**
	- Financial interest in Notion
- **Notion's Employee (Developers, designers, marketers, etc.)**
	- Develop and market Notion
- **Stakeholders of product/business made by a Notion's user**
	- Documentation of the product made with Notion (for example a PDF generated with Notion)
	- Website or portfolio made with Notion

## Contribution statement:

We worked together as a team on this team like we had done on the project. We met during our regular team meetings and assigned tasks to each member. Then we collaborated over gitlab to finalize the report. The commits were reviewed by other team members before they were added to the main branch. The artefacts for the assignment can be be found in the directory. Each member of the team worked on multiple facets of the assignment so that everyone can get an idea of the whole picture.


**Work division:**

1: Aayush

2.1: Luke + Tamara

2.2: Varun + Aayush

2.3: Rishabh + Varun

2.4 User stories: Tamara, Acceptance tests: Tamara + Rishabh

* Put your work on gitlab.
* Internal deadline among the group: **Oct 13th**


**link to significant contribution**
Question 1.1 and 1.2 [Aayush]:

Question 2.1 [Luke][Tamara]:

Question 2.2 [Varun][Aayush]:

Question 2.3 [Rishabh][Varun]:

Question 2.4.1 and 2.4.2 [Tamara][Rishabh]:


Typo correction, admin work:


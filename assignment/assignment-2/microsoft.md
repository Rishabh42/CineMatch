### G1: Make clear what the system can do.

Notion AI provides suggestions about what the user can do every time it is invoked, as can be seen in Figure 1. While the user can type in a free prompt, Notion AI clearly informs the users about all possible functions it can carry out.
![](/assignment/assignment-2/artifacts/g1.png)
_Figure 1: Notion AI suggestions on hitting Space_

### G2: Make clear how well the system can do what it can do. 

Since Notion AI uses GPT-3.5 under the hood, it shares similar shortcomings with ChatGPT - the generated content may be inaccurate or misleading. This limitation is acknowledged in each response, as shown in Figure 2.
![](/assignment/assignment-2/artifacts/g2.png)
_Figure 2: Notion AI warns of limitations of generated responses_

### G3: Time services based on context.

Notion AI is based on GPT-3.5, which like other language models, is not designed to provide real-time information or location-based guidance. It operates based on the input it receives and generates responses accordingly. Therefore, for time-sensitive tasks, Notion AI may not be the most suitable tool.

### G4: Show contextually relevant information.

Notion AI tweaks its AI suggestions based on the context by anticipating what the user needs at each step in the interaction. Here are a few scenarios where Notion AI shows contextually relevant information, when the user hits the `Space` key to call Notion AI:
- Starting a new page: Notion AI prioritizes suggestions for drafting functions like brainstorming ideas or writing a story, essay, blog post and more (see Image 1)
- Adding a new block around existing content: Notion AI prioritizes generating more ideas or extracting relevant information from the content, like "Continue writing", "Summarize" and "Find action item".
![](/assignment/assignment-2/artifacts/g4.1.png)
_Figure 3: Notion AI suggestions with existing content_
- Selecting a block of text: Notion AI gives precedence to providing suggestions related to editing the selected content, including changing the tone of or improving the writing, or fixing spelling and grammar mistakes.
![](/assignment/assignment-2/artifacts/g4.2.png)
_Figure 4: Notion AI suggestions on selecting text_


Source: [The design thinking behind Notion AI](https://www.notion.so/help/guides/using-notion-ai)

### G5: Match relevant social norms

For the main functions provided by Notion AI, social norms do not particularly come into play. The AI functions are directly performed on the text, without much extra dialogue between the AI and user. However, the user has a certain amount of control over the nature of the generated content, for example, by defining the tone of the content. 

### G6: Mitigate social biases

One of the current limitations of Notion AI is the possibility of bias in the outputted responses, a limitation inherent to the GPT-3.5 model. While measures are put in place to reduce biases, especially during model training, the model may still exhibit biased behavior or reinforce certain stereotypes. 

### G7: Support efficient invocation

Notion AI can be invoked simply by hitting the `Space` key, which will open the prompt as seen in Figure 1. Similarly whenever a block of text is selected, the first option that appears is "Ask AI", highlighted in a different color.

![](/assignment/assignment-2/artifacts/g7.png)
_Figure 5: Pop up displayed on selecting text_

### G8: Support efficient dismissal

Notion AI allows the user to easily dismiss the answer if the user is not satisfied through the "Discard" option present in the output for all generates responses (Figure 6).

![](/assignment/assignment-2/artifacts/g8.png)
_Figure 6: Notion AI output and further suggestions after changing tone of the selected text to "Professional"_

### G9: Support efficient correction

Depending on the kind of operation, Notion AI offers features to edit the generated content or to redo the operation. For example, in Figure 6, Notion AI provides the option to make the generates response longer or to try again. It is also possible to type in a new prompt in plain language ("Tell AI what to do next...") to refine or edit the response as one desires. For example, one could prompt Notion AI to convert the output to a bulleted list or table format.

### G10: Scope services when in doubt

Since Notion AI follows predefined instructions, it does not engage in disambiguation or gracefully degrade its services when uncertain about a user's goals

### G11: Make clear why the system did what it did

Notion AI is an assistant that follows predefined instructions to provide responses based on user inputs. It does not have the ability to explain why it generated a specific output or provide transparency into its decision-making process. Its responses are based solely on the instructions it has been programmed with.

### G12: Remember recent interactions

Searches are saved only if the user accepts the suggestions given by the AI and can be used for reference later. However, it does not save the prompts in a ‘history’ list format. It does not have the ability to retain information from previous interactions or remember specific user inputs. Each interaction with Notion AI is treated as an isolated event, and it does not have the capability to recall past information or context.

### G13: Learn from user behavior

Notion AI does not learn from user behavior. It follows predefined instructions and does not have the ability to adapt or improve based on user interactions.

### G14: Update and adapt cautiously

Notion AI does not limit disruptive changes when updating and adapting the AI system's behaviors.

### G15: Encourage granular feedback

Yes, user can provide granular feedback and also give a thumbs up/down rating to the text prompts.

![](/assignment/assignment-2/artifacts/g15.png)
_Figure 6: Feednack suggestion_

### G16: Convey the consequences of user actions

No

### G17: Provide global controls

No

### G18: Notify users about changes

Doesn’t explicitly notify people but new releases can be tracked through their blog posts or Twitter accounts


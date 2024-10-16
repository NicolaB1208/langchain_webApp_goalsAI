# GoalsAI Coach #
*The AI assistant that will help you plan and reach your goals.*


![GoalsAI Coach banner](https://github.com/user-attachments/assets/3fa6e962-dec9-481c-91a6-b76ccd5bc986)

## Intro ##
A conversational chatbot that guides you through a series of steps to set and achieve your goals.

Main features:
* It follows a structured conversation based on the system prompt.
* Langchain tools to: launch queries on the knowledge base, save user data, and update goal cards in the UI.
* Llamaindex to query the knowledge base.
* Interactive UI that updates based on the user's conversation with the AI.

*This is a personal project I deployed in February 2024.*

## How it works ##

`app.py`:
* Basic signup / login / logout functionality — saving and checking data in an SQLite database.

* Route `/ask`:
  Receives the transcript of the user message and runs the Langchain agent.

### Agent tools: ###
* Query the knowledge base - function in `answer_questions.py`
* Load and check user's saved goals - functions in `goal_management.py` to query `user_goals.db`
* Add goals
* Modify goals

### React components ###
* `index.js` fetches regularly from `/goals` to query the user's goals. Receives a JSON of the goals and modifies HTML to show the goals in the UI.
* `chatbot.js` handles all chatbot conversations - fetches the `/ask` route to get replies from AI and renders the thinking animation.

### Tech stack ###

* React frontend
* Webpack bundles the frontend code
* Node.js manages frontend dependencies
* Flask backend handles requests


# GoalsAI coach #
*The AI assistant that will help you plan and reach your goals.*

## Intro ##
![GoalsAI Coach banner](https://github.com/user-attachments/assets/3fa6e962-dec9-481c-91a6-b76ccd5bc986)

A conversational chatbot that guide your trough a series of steps to set and achieve your goals. 

Main features:
* It follows a structured conversation based on the system prompt
* Langchain tools to: launch the query of knowledge base, save the user's data and update the goal cards in the UI.
* Llamaindex to query the knowledge base
* Interactive UI that updates based on the user conversation with the AI
  
*This is a personal project I deployed in February 2024.*

## How it works ##

`app.py`:
* Basic signup / login / log out function -- saving and checking data to SQLite database
  
* route `/ask`
  Receive the transcript of the user message and run the langchain agent

### Agent tools: ###
* Query the knowledge base - function in `answer_questions.py`
* Load and check user's saved goals - functions in `goal_management.py` to query `user_goals.db`
* Add goals 
* Modify goals

### React components ###
* `index.js` fetches regulary `/goals` to query the user's goals. Receive a json of the goals and modify html to show the goals in the UI
* `chatbot.js` handles all the chatbot conversation - fetch the `/ask` route to get replies from AI, render the thinking animation

  


### Tech stack ###

* React frontend
* Webpack bundles the frontend code
* Node.js manage frontend dependencies
* Flask backend handling requests

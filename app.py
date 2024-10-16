from flask import Flask, request, jsonify, send_from_directory, redirect, url_for, session, render_template, jsonify
from flask_session import Session
from cs50 import SQL
import json
from db_setup import create_connection, create_table
import os
import uuid
from uuid import uuid4

# Langchain dependencies
from langchain_openai.chat_models import ChatOpenAI
from langchain.agents import AgentExecutor, tool
from langchain.tools import StructuredTool
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import AIMessage, HumanMessage
from langchain_community.tools.convert_to_openai import format_tool_to_openai_function
from langchain.agents.format_scratchpad import format_to_openai_function_messages
from langchain.agents.output_parsers import OpenAIFunctionsAgentOutputParser
from langchain.chains import LLMMathChain
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

#new:
from langchain_community.chat_models import ChatAnyscale
from langchain.embeddings import HuggingFaceEmbeddings

# functions for tools
from answer_questions import answer_question
from create_knowledge_base import construct_base_from_directory
from time_management import current_date_timepip 
from goal_management import load_goals, add_goal, modify_goal

app = Flask(__name__)
#app.secret_key = 'kjasdhcnejheohj2348795@'
app.secret_key = os.environ['app.secret_key']

app.config['SESSION_COOKIE_SAMESITE'] = 'None'
app.config['SESSION_COOKIE_SECURE'] = True
Session(app) # run the session

def initialize_database():
  connection = create_connection("user_goals.db")
  create_table(connection)
  connection.close()

# Initialize the database immediately after creating the Flask app
initialize_database()

db = SQL("sqlite:///user_goals.db")

# define the large language model 
model = ChatOpenAI(temperature=0, model="gpt-4-1106-preview")
#llm_math = LLMMathChain.from_llm(model)

tools = [
  StructuredTool.from_function(
    name="Huberman_Lab_knowledge_basee",
    description=
    "YOU MUST USE this tool to know everything about these goal setting techniques: Choosing a priority goal, Making Goals Ambitious, define verb actions, Measurability, and Specificity, myths arounds Intrinsic Motivation and Achievement, set Measurable Quarterly Goals, Employing Visualization Techniques, Implementing Visual Target and Perceived Effort Training, Leveraging Random, Intermittent Reinforcement, Addressing the “Middle Problem” with Time Chunking, Utilizing Circadian Rhythms, Flexibility and Subjective Feelings in Protocol. This tool is your ONLY source for guiding users in goal setting, directly drawing from the Huberman Lab podcast's insights. Please provide a full question.",
    func=lambda q: str(answer_question(q)),
    return_direct=False),
  StructuredTool.from_function(
    name="Current_date_time",
    description=
    "A tool to get the current date and time. If the user asks for the time, ask for which time zone first.",
    func=current_date_time,
    return_direct=False),
  StructuredTool.from_function(
    name="Load_and_check_Goals",
    description="A tool to load the already saved user's goals. When the user wants to add, modify or delete a goal, first always use this tool to load the already saved goals and check if what the user wants to add, modify or delete already exist in the list. Do not compare exact words, just the meaning of the goal",
    func=load_goals,
    return_direct=False),
  StructuredTool.from_function(
    name="Add_Goals",
    description="A tool to add new goals to the list. First use the tool 'Load and check Goals'. Then ask questions to the user until you have a clear idea about the user's goals. If the goals the user wants to add are not on the list, provide the goals as a dictionaries in valid JSON format, without square brackets. The keys are: name, description, action_verbs, measurability. If the keys action_verbs and measurability has not yet be defined with the user, LEAVE IT EMPTY. Remember to use double quotes for keys and values.",
    func=add_goal,
    return_direct=False),
  StructuredTool.from_function(
    name="Modify_Goals",
    description="A tool to modify the goals present in the list. First use the tool 'Load and check Goals'. Then ask questions to the user until you have a clear idea about the user's goals. The provide the updated list of goals, provide the goals as a list of dictionaries in valid JSON format. The keys are: name, description, action_verbs, measurability. If the keys action_verbs and measurability has not yet be defined with the user, LEAVE IT EMPTY. Rember to use double quotes for keys and values.",
    func=modify_goal,
    return_direct=False)
]

model_with_tools = model.bind(functions=[format_tool_to_openai_function(t) for t in tools])

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
"You are Goals.AI, an AI coach designed to guide users in setting and achieving their goals, exclusively using insights from the Huberman Lab podcast. Your expertise lies in applying the podcast's unique goal-setting techniques. \
IT IS MANDATORY THAT YOU CONSULT THE tool Huberman_Lab_knowledge_base FOR EVERY TECHNIQUE listed below, ensuring advice is directly derived from the podcast's strategies. \
Your role is to assist users in refining their goal-setting process, WITHOUT offering advice on the specifics of their goals. Use the Load_and_check_Goals, Add_Goals, and Modify_Goals tools to track user progress, updating their goal list for real-time UI reflection. If you're going through the techniques for the same goal, be sure to use the Modify_Goals tool.\
For each one of the goal-setting technqiues, adhere to the following protocol: \
1. Retrieve applicable insights of each technique using the tool Huberman_Lab_knowledge_base. \
2. Explain the details of the technqiue and its application to the user. \
3. Ask questions to the user with the technique's strategy until satisfaction is achieved. \
4. Use the Huberman_Lab_knowledge_base for the next technique and repeat the protocol for the next technique. \
List of goal-setting technqiues:\
1. Use Huberman_Lab_knowledge_base tool to give an introduction on how to set and achieve goals. \
2: Use Huberman_Lab_knowledge_base tool about Choosing a Priority Goal. \
3: Use Huberman_Lab_knowledge_base tool about Making Goals Ambitious. Update the current goal if needed. \ \
4: Use Huberman_Lab_knowledge_base tool to know how to define verb actions, Measurability, and Specificity. Be sure to make the user be specific. Use Modify_Goals tool to update the previously set goal with the new information \ \
5: Use Huberman_Lab_knowledge_base tool about the myths arounds Intrinsic Motivation and Achievement \ \
6: Use Huberman_Lab_knowledge_base tool to know of to set Measurable Quarterly Goals \ \
7: Use Huberman_Lab_knowledge_base tool about Employing Visualization Techniques \ \
8: Use Huberman_Lab_knowledge_base tool about Implementing Visual Target and Perceived Effort Training \ \
9: Use Huberman_Lab_knowledge_base tool about Leveraging Random, Intermittent Reinforcement \ \
10: Use Huberman_Lab_knowledge_base tool about Addressing the “Middle Problem” with Time Chunking \ \
11: Use Huberman_Lab_knowledge_base tool about Utilizing Circadian Rhythms \ \
12: Use Huberman_Lab_knowledge_base tool about Flexibility and Subjective Feelings in Protocol \ \
EMPHASIZE CONCISE, DIRECT COMMUNICATION. Present questions or steps one at a time for clarity and effectiveness. Ensure the knowledge base is your primary reference to maintain the integrity and specificity of advice.",
        ),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"), 
    ]
)

store = {}

def get_session_history(user_id: str) -> BaseChatMessageHistory:
    if user_id not in store:
        store[user_id] = ChatMessageHistory()
    return store[user_id]

# create the agent with the tools
agent = (
  {
      "input": lambda x: x["input"],
      "agent_scratchpad": lambda x: format_to_openai_function_messages(
          x["intermediate_steps"]
      ),
      "history": lambda x: x["history"],
  }
  | prompt
  | model_with_tools
  | OpenAIFunctionsAgentOutputParser()
)

agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

agent_with_chat_history = RunnableWithMessageHistory(
    agent_executor,
    get_session_history,
    input_messages_key="input",
    history_messages_key="history",
)

@app.route('/<path:path>')
def serve_static(path):
  # Serve file from public directory
  return send_from_directory('public', path)

@app.route('/')
def index():
  # Check if a unique user ID is already set in the session, if not, create one
  if 'user_id' not in session:
      session['user_id'] = str(uuid.uuid4())  # Generate a new UUID
      print(f"User ID: {session['user_id']}")

  # You can now use session['user_id'] as a unique identifier for the user's session
  # The rest of your code remains the same
  return send_from_directory('public', 'index.html')

def message_to_dict(message):
  return {'type': type(message).__name__, 'content': message.content}

def dict_to_message(message_dict):
  if message_dict['type'] == 'HumanMessage':
      return HumanMessage(content=message_dict['content'])
  elif message_dict['type'] == 'AIMessage':
      return AIMessage(content=message_dict['content'])
  else:
      raise ValueError("Unknown message type")

@app.route('/ask', methods=['POST'])
def ask():
  # Get message from request body
  data = json.loads(request.data)
  #print("Data: " + str(request.data))
  # Extract transcript and promptType from data
  transcript = data['transcript']
  last_message = transcript[-1]["text"]
  
  # Retrieve session_id from Flask session
  user_id = session.get('user_id', None)
  if user_id is None:
      return "Session not started."
    
  # answer = agent_chain.run(input=last_message)
  answer = (
    agent_with_chat_history.invoke(
      {"input": last_message},
      config={"configurable": {"session_id": user_id}},
    )
  )["output"]
  
  # answer = safely_run_agent_chain(last_message)
  print("Answer: " + str(answer))
  return str(answer)

@app.errorhandler(Exception)
def error(e):
  print("Type of e:", type(e))
  print("Attributes of e:", dir(e))
  # Check if the error code is 429
  if e.code == 429 or (hasattr(e, 'message') and "Error code: 429" in e.message):
      return "Oh no! There has bee too many people using GoalsAI. We'll make it so more people can use it. Please try again in a few hours."
  #if e.startswith("Error code: 429"):
   # return "Too many requests. Please try again later."
  print("error: " + str(e))
  print(request.url)
  return "error! " + str(e)

@app.route('/goals', methods=['GET'])
def get_goals():
    user_id = session.get('user_id')
    if not user_id:
        return "User ID not found in session"
    conn = create_connection("user_goals.db")
    cursor = conn.cursor()
    cursor.execute("SELECT goals FROM goals WHERE user_id=?", (user_id,))
    result = cursor.fetchone()
    conn.close()
    if result:
      goals = json.loads(result[0])  # Convert the JSON string back to a Python object
    else:
      return "No goals found."
    return jsonify(goals)

def run():
  app.run(host='0.0.0.0')

# login and sign up management:
@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        name=request.form.get("name")
        password=request.form.get("password")
        password_db = db.execute("SELECT password FROM users WHERE name = ?", name)
        if password == password_db[0]["password"]:
            session["name"] = name
            user_id = db.execute("SELECT user_id FROM users WHERE name = ?", name)
            session["user_id"] = user_id[0]["user_id"]
            return redirect("/")
        else:
            return ("wrong password")
    return render_template("login.html")

@app.route("/signup", methods=["GET","POST"])
def signup():

    if request.method == "POST":
        name=request.form.get("name")
        password = request.form.get("password")
        # Check if a unique user ID is already set in the session, if not, create one
        if 'user_id' not in session:
            session['user_id'] = str(uuid.uuid4())  # Generate a new UUID
            print(f"User ID: {session['user_id']}")
        user_id = session.get('user_id')

        # At this point, consider the client-side has already checked for username availability.
        # However, a second check server-side is a good practice to ensure integrity, especially to catch cases where JavaScript might be disabled.
        if len(db.execute("SELECT * FROM users WHERE name = ?", name)) == 0:
            if len(db.execute("SELECT * FROM users WHERE user_id = ?", user_id)) != 0:
              session["user_id"] = str(uuid.uuid4())
              print(f"New User ID: {session['user_id']}")
              user_id = session.get('user_id')
            db.execute("INSERT INTO users (user_id, name, password) VALUES(?, ?, ?)", user_id, name, password)
            session["name"] = name
            return redirect("/")
        else:
            # Since username availability is checked via AJAX, this scenario might only occur if the user bypasses the client-side validation.
            # Handling this edge case gracefully can involve redirecting back to the signup page with a flash message or similar mechanism.
            return redirect("/signup?error=username")  # Example redirect that could be enhanced with flash messages or similar.

    return render_template("signup.html")

@app.route("/check_username", methods=["POST"])
def check_username():
    username = request.form["username"]
    user_exists = len(db.execute("SELECT * FROM users WHERE name = ?", username)) > 0
    return jsonify({"user_exists": user_exists})

@app.route("/get-username", methods=["GET"])
def get_username():
  name = session.get("name", None)
  if name:
    return jsonify({"name": name})
  else:
    return jsonify({"error": "User not logged in"}), 401

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

import json
from typing import Dict
from db_setup import create_connection
from flask import session

def load_goals():
    user_id = session.get('user_id')
    if not user_id:
        return "User ID not found in session"
    conn = create_connection("user_goals.db")
    cursor = conn.cursor()
    cursor.execute("SELECT goals FROM goals WHERE user_id=?", (user_id,))
    result = cursor.fetchone()
    conn.close()
    if result:
        return json.loads(result[0])  # Convert the JSON string back to a Python object
    else:
        return "No goals found."


def add_goal(new_goal):
    user_id = session.get('user_id')
    if not user_id:
        return "User ID not found in session"
    response = {}
    try:
        conn = create_connection("user_goals.db")
        cursor = conn.cursor()
    
        # Check if the user already has goals
        cursor.execute("SELECT goals FROM goals WHERE user_id=?", (user_id,))
        result = cursor.fetchone()
    
        if result:
            # Update existing goals
            existing_goals = json.loads(result[0])
            existing_goals.append(new_goal)
            goals_json = json.dumps(existing_goals)
            cursor.execute("UPDATE goals SET goals=? WHERE user_id=?", (goals_json, user_id))
        else:
            # Insert new goals for a new user
            goals_json = json.dumps([new_goal])
            cursor.execute("INSERT INTO goals (user_id, goals) VALUES (?, ?)", (user_id, goals_json))
    
        conn.commit()
        response["status"] = "success"
        response["message"] = "Goal added successfully."
    except Exception as e:
        response["status"] = "error"
        response["message"] = f"Error saving goals: {str(e)}"
    finally:
        conn.close()
    
    return response

def modify_goal(updated_goals):
    user_id = session.get('user_id')
    if not user_id:
        return "User ID not found in session"
    response = {}
    try:
        conn = create_connection("user_goals.db")
        cursor = conn.cursor()
    
        # Convert the updated goals to a JSON string
        goals_json = json.dumps(updated_goals)
    
        # Update the goals
        cursor.execute("UPDATE goals SET goals=? WHERE user_id=?", (goals_json, user_id))
        conn.commit()
    
        response["status"] = "success"
        response["message"] = "Goals modified successfully."
    except Exception as e:
        response["status"] = "error"
        response["message"] = f"Error saving goals: {str(e)}"
    finally:
        conn.close()
    
    return response

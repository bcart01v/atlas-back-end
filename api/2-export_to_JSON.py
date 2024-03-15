#!/usr/bin/python3
"""
This module establishes a connection to jsonplaceholder to retrieve a user
and their todo list. It emphasizes the importance of error handling when
accessing API endpoints to inform the user about any issues retrieving data.
"""

import json
import requests
import sys


USERS_URL = "https://jsonplaceholder.typicode.com/users/"
TODOS_URL = "https://jsonplaceholder.typicode.com/todos?userId="


def get_JSON_export(employee_id):
    """
    Fetches a user and their todo list from the JSONPlaceholder API and exports
    the data to a CSV file named after the user's ID.

    Parameters:
    - employee_id: The ID of the employee to retrieve information for.
    """
    user_response = requests.get(f"{USERS_URL}{employee_id}")
    if user_response.status_code != 200:
        print("Failed to retrieve employee information.")
        return

    user_data = user_response.json()
    employee_name = user_data.get('name')
    if not employee_name:
        print("Employee not found.")
        return

    username = user_data.get('username')
    if not username:
        print("Employee does not have a username set.")
        return

    todos_response = requests.get(f"{TODOS_URL}{employee_id}")
    if todos_response.status_code != 200:
        print("Failed to retrieve TODO list. Please check your parameters.")
        return

    todos = todos_response.json()

    # Prepare data for JSON
    todo_json = []
    for item in todos:
        todo_json.append({
            "task": item["title"],
            "completed": item["completed"],
            "username": username
        })

    # Prepare JSON srtucture
    json_data = {str(employee_id): todo_json}

    # Write json_data to .json
    with open(f"{employee_id}.json", mode='w') as file:
        json.dump(json_data, file, indent=4)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Please enter the employee ID.")
        sys.exit(1)

    try:
        employee_id = int(sys.argv[1])
    except ValueError:
        print("Employee ID must be an integer.")
        sys.exit(1)

    get_JSON_export(employee_id)

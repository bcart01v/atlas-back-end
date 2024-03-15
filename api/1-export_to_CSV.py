#!/usr/bin/python3
"""
This module establishes a connection to jsonplaceholder to retrieve a user
and their todo list. It emphasizes the importance of error handling when
accessing API endpoints to inform the user about any issues retrieving data.
"""

import csv
import requests
import sys

# Constants should be at the top of the file
USERS_URL = "https://jsonplaceholder.typicode.com/users/"
TODOS_URL = "https://jsonplaceholder.typicode.com/todos?userId="

def get_csv_export(employee_id):
    """
    Fetches a user and their todo list from the JSONPlaceholder API and exports
    the data to a CSV file named after the user's ID.
    
    Parameters:
    - employee_id: The ID of the employee to retrieve information for.
    """
    user_response = requests.get(f"{USERS_URL}{employee_id}")
    if user_response.status_code != 200:
        print("Failed to retrieve employee information. Please check parameters.")
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
    csv_file_name = f"{employee_id}.csv"

    with open(csv_file_name, mode='w', newline='') as file:
        writer = csv.writer(file, quoting=csv.QUOTE_ALL, lineterminator='\n') 
        writer.writerow(["USER_ID", "USERNAME", "TASK_COMPLETED_STATUS", "TASK_TITLE"])
        for task in todos:
            writer.writerow([employee_id, username, task['completed'], task['title']])

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Please enter the employee ID.")
        sys.exit(1)

    try:
        employee_id = int(sys.argv[1])
    except ValueError:
        print("Employee ID must be an integer. Please enter a valid Employee ID.")
        sys.exit(1)

    get_csv_export(employee_id)

#!/usr/bin/python3
""" Module Documentation
This module establishes a connection to jsonplaceholder
And gets a user, and todo list (if applicable).
I've worked with many API's, and it's always good practice
To have error messages when accessing any point of the API
When getting data, so the end user knows something happened
If either the object is not returned, or the specific requested
field is blank.
"""


import requests
import sys


def get_employee_todo_progress(employee_id):
    # Establish a connection to our API
    USERS = "https://jsonplaceholder.typicode.com/users/"
    TODOS = "https://jsonplaceholder.typicode.com/todos?userId="

    # Get the User's Name
    user_response = requests.get(f"{USERS}{employee_id}")
    if user_response.status_code != 200:
        print("Failed to retrieve employee information")
        print("please check parameters")
        return

    employee_name = user_response.json().get('name')
    if not employee_name:
        print("Employee not found.")
        return

    # Get the ToDo list for the specific employee.
    todos_response = requests.get(f"{TODOS}{employee_id}")
    if todos_response.status_code != 200:
        print("Failed to retrieve TODO list")
        print("please check your parameters")
        return

    todos = todos_response.json()

    # Filtering completed tasks
    completed_tasks = [task for task in todos if task['completed']]

    # Printing the TODO list progress
    print(f"Employee {employee_name} is done with tasks \
        ({len(completed_tasks)}/{len(todos)}):")
    for task in completed_tasks:
        print(f"\t {task['title']}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Please enter Employee ID.")
        sys.exit(1)

    try:
        employee_id = int(sys.argv[1])
    except ValueError:
        print("This shouldn't have happened. What did you do?")
        sys.exit(1)

    get_employee_todo_progress(employee_id)

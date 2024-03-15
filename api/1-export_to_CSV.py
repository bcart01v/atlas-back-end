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

import csv
import requests
import sys


def get_csv_export(employee_id):
    # Establish a connection to our API
    USERS = "https://jsonplaceholder.typicode.com/users/"
    TODOS = "https://jsonplaceholder.typicode.com/todos?userId="

    # Get the User's Name
    user_response = requests.get(f"{USERS}{employee_id}")
    if user_response.status_code != 200:
        print("Failed to retrieve employee information"
              "please check parameters")
        return

    user_data = user_response.json()

    employee_name = user_data.get('name')
    if not employee_name:
        print("Employee not found.")
        return

    username = user_data.get('username')
    if not username:
        print("Employee does not have Username set.")
        return

    # Get the ToDo list for the specific employee.
    todos_response = requests.get(f"{TODOS}{employee_id}")
    if todos_response.status_code != 200:
        print("Failed to retrieve TODO list"
              "please check your parameters")
        return

    # Set the Todo List
    todos = todos_response.json()

    # Create the CSV file.
    # This should verify if there's data first, otherwise we're
    # creating blank excel files.
    csv_file = f"{employee_id}.csv"

    # Write to the CSV File
    with open(csv_file, mode='w', newline='') as file:
        writer = csv.writer(file, quoting=csv.QUOTE_ALL)

        # Write the header's
        writer.writerow(["USER_ID", "USERNAME",\
            "TASK_COMPLETED_STATUS", "TASK_TITLE"])

        # Write the tasks
        for task in todos:
            writer.writerow([employee_id, username,\
                task['completed'], task['title']])


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Please enter Employee ID.")
        sys.exit(1)

    try:
        employee_id = int(sys.argv[1])
    except ValueError:
        print("This shouldn't have happened. What did you do?")
        sys.exit(1)

    get_csv_export(employee_id)

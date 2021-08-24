# Vacation Request API

## Description

HTTP API that allows employees to make vacation requests and provides managers with an overview of all vacation requests and allows them to decline or approve requests.

## Requirements

- Python 3.x
- flask
- flask_restful
- flask-sqlalchemy

Ensure requirements are met by checking Python version and installing dependencies with these commands
'''
python --version
pip install flask
pip install flask-restful
pip install flask-sqlalchemy
'''

## Base URL

"http://127.0.0.1:5000/"

## API Routes

Flask-restful segments different routes into a 'Resource' class. Each 'Resource' can have only one HTTP method type attached to it.

    ex. ToDo Resource can only have one GET method, to list or GET all ToDo objects, another ToDoList Resource and route would be needed

Therefore, the following resources will have different routes and use cases

### Vacation Request [GET, PUT, PATCH, DELETE]
url: '/vacation'

description: CRUD controller for Vacation Request Model

GET: 
    - returns Vacation Request Model data
    - requires entire signature of Vacation Request object, no NULL values
    - only id is used of data in signature

PUT:
    - creates Vacation Request Model
    - requires entire signature of Vacation Request object, no NULL values
    - Business logic of Vacation Request is checked in this function

PATCH:
    - updates status variable of Vacation Request Model
    - requires entire signature of Vacation Request object, no NULL values
    - only id is used of data in signature

DELETE:
    - deletes Vacation Request Model
    - requires entire signature of Vacation Request object, no NULL values
    - only id is used of data in signature

### Vacation Request Employee [GET]
url: '/vacation/employee'

description: Shows all Vacation Requests of individual employee

GET: 
    - returns list of Vacation Requests from given worker id
    - requires entire signature of Vacation Request object, no NULL values
    - only author is used of data in signature

### Vacation Request Employee Filter [GET]
url: '/vacation/employee/filter'

description: Filters Vacation Requests of individual employee by status

GET: 
    - returns list of Vacation Requests from given worker id and status
    - requires entire signature of Vacation Request object, no NULL values
    - author and status is used from signature

### Vacation Request Remaining [GET]
url: '/vacation/employee/remaining'

description: Calculate the number of vacation days remaining for employee

GET: 
    - returns integer of remaining vacation days
    - requires entire signature of Vacation Request object, no NULL values
    - author is used from signature
    - does not count Federal Holidays and weekend days

### Vacation Request Manager [GET]
url: '/vacation/manager'

description: Shows all Vacation Request of individual manager

GET: 
    - returns list of Vacation Requests from given manager id
    - requires entire signature of Vacation Request object, no NULL values
    - resolved_by is used from signature

### Vacation Request Manager Filter [GET]
url: '/vacation/employee/remaining'

description: Filters Vacation Requests of individual manager by status

GET: 
    - returns list of Vacation Requests from given manager id and status
    - requires entire signature of Vacation Request object, no NULL values
    - resolved_by and status is used from signature

### Vacation Request Manager Overlap [GET]
url: '/vacation/employee/remaining'

description: Shows overlapping Vacation Request based on another Vacation Request

GET: 
    - returns list of Vacation Requests that overlap with Vacation Request provided
    - requires entire signature of Vacation Request object, no NULL values
    - vacation_start_date and vacation_end_date is used from signature

## Testing

Unit tests are attached in tests folder. 

To run tests:
    - Run main.py to activate API
    - Run vacation_api_test.py first as this creates test data
    - Other tests can be ran in any order
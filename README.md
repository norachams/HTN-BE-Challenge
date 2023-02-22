# HTN-Backend-Challenge
This is my submission for the Hack the North Backend challenge. 
This was my first project using SQLite with Flask and making APIs, so there was a lot to learn. I learned alot building this and really enjoyed it. These are the links that helped me.
- [To understand how to make a connection and create tables with our data](https://www.sqlitetutorial.net/sqlite-python/creating-tables/)
- [To understand how to use SQLite with Flask](https://www.digitalocean.com/community/tutorials/how-to-use-an-sqlite-database-in-a-flask-application)
- [To understand how to use Flask RESTful APIs](https://flask-restful.readthedocs.io/en/latest/)

### Libraries and dependencies used
- Flask
- sqlite3
- Flask RESTful APIs 

## Setup:

Create and activate virtual environment using virtualenv
```bash
$ python -m venv python3-virtualenv
$ source python3-virtualenv/bin/activate
```

Start flask development server
```bash
$ export FLASK_ENV=development
$ flask run
```

## Users Endpoints and API routes:
### All Users Endpoint
``` GET http://127.0.0.1:5000/users ``` Retrieves data for all users

### User Information Endpoint
``` GET http://127.0.0.1:5000/20``` Retrieves all data for a given user, where '20' is the user_id

### Updating User Input
``` PUT http://127.0.0.1:5000/users/20``` Given data in a JSON format it will return the updated hacker data as the response.

### Skills Endpoints
``` GET http://127.0.0.1:5000/skills``` Retrieves all skills and their frequencies 

``` GET http://127.0.0.1:5000/skills?min_frequency=15&max_frequency=20``` Retrieves all skills in between the min and max frequencies given


## Improvements:
- Connecting the backend to a frontend so it can be easier to interact with the user endpoints
- I would've liked to add some tests but I did not have enough time 
- Creating endpoints to retrieve the information of each hacker registred in a specific event. So if we want to see who registred for an event and how many hackers are registred. 
- Adding some error handling troughout the api so we can get more specific error. 

- If I had proir knowlodge of how to use SQL and rest APIs I feel like I would have finished it faster and implemented more endpoints to make it better. Nevertheless it was a great and fun learning opportunity. Thank you for your consideration. 

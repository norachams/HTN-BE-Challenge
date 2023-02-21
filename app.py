from flask import Flask , json

app = Flask(__name__)

import sqlite3
import json

# Reading data from JSON file
with open('data.json', 'r') as d:
    data = json.load(d)

# Connecting to database and creating table
conn = sqlite3.connect('users.db')
c = conn.cursor()

# Drop tables if they already exist
c.execute('''DROP TABLE IF EXISTS users''')
c.execute('''DROP TABLE IF EXISTS skills''')


#Creating table for users
c.execute('''
    CREATE TABLE users (
        rowid INTEGER PRIMARY KEY,
        name TEXT,
        company TEXT,
        email TEXT,
        phone TEXT
    )
''')

          
# Creating table for skills
c.execute('''
    CREATE TABLE skills (
        users_id INTEGER,
        skill TEXT,
        rating INTEGER
    )
''')         

# Insert data into table
for i, users in enumerate(data):
    c.execute('''
        INSERT INTO users (name, company, email, phone) VALUES (?, ?, ?, ?)
    ''', (users['name'], users['company'], users['email'], users['phone']))
    users_id = c.lastrowid
    for skill in users['skills']:
        c.execute('''
            INSERT INTO skills (users_id, skill, rating) VALUES (?, ?, ?)
        ''', (users_id, skill['skill'], skill['rating']))


# Save changes and close database connection
conn.commit()
conn.close()


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


# All Users Endpoint use localhost:5000/users/
@app.route("/users")
def get_users():
    try:
        conn = sqlite3.connect('users.db')
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute('SELECT * FROM users')
        users = c.fetchall()
        user_list = []
        for user in users:
            user_dict = dict(user)
            c.execute('SELECT skill, rating FROM skills WHERE users_id = ?', (user_dict['rowid'],))
            skills = c.fetchall()
            skill_list = []
            for skill in skills:
                skill_dict = dict(skill)
                skill_list.append(skill_dict)
            user = {'name': user_dict['name'], 'email': user_dict['email'], 'skills': skill_list}
            user_list.append(user)
        conn.close()
        response = {'users': user_list}
        return json.dumps(response)
    except Exception as e:
        return f"An error occurred: {e}"

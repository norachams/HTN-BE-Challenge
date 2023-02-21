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
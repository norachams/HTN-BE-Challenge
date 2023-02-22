from flask import Flask, json, request, jsonify
from flask_restful import Resource, Api
import sqlite3
import json

app = Flask(__name__)
api = Api(app)

# Reading data from JSON file
with open('data.json', 'r') as d:
    data = json.load(d)

#making a funtion to populate and connect database    
def connect_db():
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

connect_db()

########################################## Defining APIs ##########################################

#this is the defualt when you first run it
class HelloWorld(Resource):
    def get(self):
        return 'Hack The North Backend Challenge By Nora Chamseddin'

# This is for "ALL USER ENDPOINTS [1]"
class All_Users(Resource):
       def get(self):
            conn = sqlite3.connect('users.db')
            c = conn.cursor()
            c.execute('SELECT * FROM users')
            users = c.fetchall()
            result = []
            for user in users:
                user_id, name, company, email, phone = user
                user_skills = c.execute('SELECT * FROM skills WHERE users_id = ?', [user_id]).fetchall()
                user_skills = [{"name":skill[1], "rating":skill[2]} for skill in user_skills]
                result.append({
                    "name": name,
                    "email": email,
                    "phone": phone,
                    "company": company,
                    "skills": user_skills
                })
            return jsonify({"users": result})
       

# using the user id  "USER INFORMATION ENDPOINT"[2] 
class Choose_User(Resource):
      def get(self, user_id):
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        # Get user details
        c.execute('SELECT * FROM users WHERE rowid = ?', (user_id,))
        user = c.fetchone()
        user_id, name, company, email, phone = user
        # Get user skills
        c.execute('SELECT skill, rating FROM skills WHERE users_id = ?', (user_id,))
        skills = [{"name": skill, "rating": rating} for skill, rating in c.fetchall()]
        # Construct user object
        user_obj = {
            "name": name,
            "email": email,
            "phone": phone,
            "company": company,
            "skills": skills
        }
        return jsonify(user_obj)

# given json format data "UPDATE A SPECIFIC USER ENDPOINT" [3]
      def put(self, user_id):
        data = request.get_json() # Get the data from the request
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute('UPDATE users SET name = ?, company = ?, email = ?, phone = ? WHERE rowid = ?', 
                  (data['name'], data['company'], data['email'], data['phone'], user_id))
        conn.commit()

        # Update the user's skills in the database
        if 'skills' in data:
            for skill in data['skills']:
                # Check if the skill already exists for the user
                c.execute('SELECT * FROM skills WHERE users_id = ? AND skill = ?', (user_id, skill['name']))
                existing_skill = c.fetchone()

                if existing_skill is None:
                    # If the skill doesn't exist, insert it into the skills table
                    c.execute('INSERT INTO skills (users_id, skill, rating) VALUES (?, ?, ?)',
                              (user_id, skill['name'], skill['rating']))
                else:
                    # If the skill already exists, update its rating
                    c.execute('UPDATE skills SET rating = ? WHERE users_id = ? AND skill = ?',
                              (skill['rating'], user_id, skill['name']))
        
        conn.commit()

        # Get the updated user data from the database
        c.execute('SELECT * FROM users WHERE rowid = ?', [user_id])
        user = c.fetchone()
        user_id, name, company, email, phone = user
        user_skills = c.execute('SELECT * FROM skills WHERE users_id = ?', [user_id]).fetchall()
        user_skills = [{"name": skill[1], "rating": skill[2]} for skill in user_skills]
        result = {
            "name": name,
            "email": email,
            "phone": phone,
            "company": company,
            "skills": user_skills
        }
        conn.close()
        return jsonify(result)
      
# "SKILLS ENDPOINTS AND FREQUENCY" [4]
class Get_Skills(Resource):
    def get(self):
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        min_frequency = request.args.get('min_frequency')
        max_frequency = request.args.get('max_frequency')
        # with query parameters 
        # returns skills with frequency between given min and max
        if min_frequency and max_frequency:
            c.execute("SELECT skill, COUNT(*) FROM skills GROUP BY skill HAVING COUNT(*) > %s AND COUNT(*) < %s" % (min_frequency, max_frequency))
        # return skills with frequency over min
        elif min_frequency:
            c.execute("SELECT skill, COUNT(*) FROM skills GROUP BY skill HAVING COUNT(*) > %s" % (min_frequency))
        # return skills with frequence under max
        elif max_frequency:
            c.execute("SELECT skill, COUNT(*) FROM skills GROUP BY skill HAVING COUNT(*) < %s" % (max_frequency))
        # with no query parameters
        # returns all skills with frequencies of each
        else:
            c.execute("SELECT skill, COUNT(*) FROM skills GROUP BY skill")
        skills = c.fetchall()
        result = [{"name": skill[0], "Frequency": skill[1]} for skill in skills]
        return jsonify({"skills": result})

api.add_resource(HelloWorld, '/')
api.add_resource(All_Users, '/users')
api.add_resource(Choose_User, "/users/<int:user_id>")
api.add_resource(Get_Skills, "/skills")


if __name__ == '__main__':
    app.run(debug=True)






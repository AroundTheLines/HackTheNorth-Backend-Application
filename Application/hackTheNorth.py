import sqlite3
from contextlib import closing
import json
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash, jsonify

# configuration
DATABASE = '/tmp/flaskr.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'
JSON_LOCATION = "https://htn-interviews.firebaseio.com/users.json?download"

# create application
app = Flask(__name__)
app.config.from_object(__name__)

def getJSON(file):
	data = open('users.json')
	return json.load(data)

def init_db():
	with closing(connect_db()) as db:
		c = db.cursor()
		with app.open_resource('schema.sql', mode='r') as f:
			c.executescript(f.read())
		data = getJSON("users.json")
		for user in data:
			user_data = [
				user['name'],
				user['picture'],
				user['company'], 
				user['email'], 
				user['phone'], 
				user['latitude'], 
				user['longitude']
			]
			c.execute('''insert into users (name, picture, company, email, phone, latitude, longitude) values (?, ?, ?, ?, ?, ?, ?)''', user_data)
			user_id = c.lastrowid
			for skill in user['skills']:
				skill_data = [
					user_id,
					skill['name'],
					skill['rating']
				]
				c.execute('''insert into skills (userId, name, rating) values (?, ?, ?)''', skill_data)
		db.commit()

def connect_db():
	return sqlite3.connect(app.config['DATABASE'])

def get_user_data(id):
	cur = g.db.execute('select name, picture, company, email, phone, country, latitude, longitude, isAccepted, isComing, needsReimbursement from users where id=(?)', (id,))
	entries = [
		dict(name=str(row[0]), 
			picture=str(row[1]), 
			company=str(row[2]), 
			email=str(row[3]), 
			phone=str(row[4]), 
			country=str(row[5]), 
			latitude=row[6], 
			longitude=row[7], 
			isAccepted=row[8], 
			isComing=row[9], 
			needsReimbursement=row[10], 
			skills=get_skills_data(id)) for row in cur.fetchall()]
	return json.dumps(entries, ensure_ascii=False)

def get_skills_data(id):
	skills_access = g.db.execute('select name, rating from skills where userID=(?)', (id,))
	skills = [
		dict(name=str(skill_row[0]), 
			rating=str(skill_row[1])
			) for skill_row in skills_access.fetchall()]
	return skills

@app.before_request
def before_request():
	g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

@app.route('/users', methods=['GET'])
def show_users():
	cur = g.db.execute('select name, picture, company, email, phone, country, latitude, longitude, isAccepted, isComing, needsReimbursement, id from users order by id desc')
	entries = [
		dict(name=str(row[0]), 
		picture=str(row[1]), 
		company=str(row[2]), 
		email=str(row[3]), 
		phone=str(row[4]), 
		country=str(row[5]), 
		latitude=row[6], 
		longitude=row[7], 
		isAccepted=row[8], 
		isComing=row[9], 
		needsReimbursement=row[10],
		skills=get_skills_data(row[11])
		) for row in cur.fetchall()]
	return json.dumps(entries, ensure_ascii=False)

@app.route('/users/<user_id>', methods=['GET', 'PUT'])
def show_user(user_id):
	if request.method == 'PUT':
		put_data = json.loads(request.get_data())
		request_keys = put_data.keys()
		user_data = get_user_data(user_id)
		for key in request_keys:
			new_key = str(key)
			if new_key in user_data:
				# I realize this is terrible, but I had 26 minutes left. ^^;;
				if key == "name":
					g.db.execute('''update users set name=? where id=?''', [put_data[key],str(user_id,)])
				elif key == "picture":
					g.db.execute('''update users set picture=? where id=?''', [put_data[key],str(user_id,)])
				elif key == "company":
					g.db.execute('''update users set company=? where id=?''', [put_data[key],str(user_id,)])
				elif key == "email":
					g.db.execute('''update users set email=? where id=?''', [put_data[key],str(user_id,)])
				elif key == "phone":
					g.db.execute('''update users set phone=? where id=?''', [put_data[key],str(user_id,)])
				elif key == "country":
					g.db.execute('''update users set country=? where id=?''', [put_data[key],str(user_id,)])
				elif key == "latitude":
					g.db.execute('''update users set latitude=? where id=?''', [put_data[key],str(user_id,)])
				elif key == "longitude":
					g.db.execute('''update users set longitude=? where id=?''', [put_data[key],str(user_id,)])
				elif key == "isAccepted":
					g.db.execute('''update users set isAccepted=? where id=?''', [put_data[key],str(user_id,)])
				elif key == "isComing":
					g.db.execute('''update users set isComing=? where id=?''', [put_data[key],str(user_id,)])
				elif key == "needsReimbursement":
					g.db.execute('''update users set needsReimbursement=? where id=?''', [put_data[key],str(user_id,)])
				g.db.commit()
	return get_user_data(user_id)

if __name__ == '__main__':
	init_db()
	app.run()
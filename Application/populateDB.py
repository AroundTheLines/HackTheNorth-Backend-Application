import json
import urllib

#def getJSON(url):
#	response = urllib.urlopen(url)
#	data = json.load(response)
#	return data

def getJSON(file):
	data = open('users.json')
	return json.load(data)

#def populate(url, db):
#	data = getJSON(url)
#	for user in data:
#		if 'country' in user:
#			print "1"
#			db.cursor().execute("""insert into users (name, picture, company, email, phone, country, latitude, longitude) values (?, ?, ?, ?, ?, ?, ?, ?)""", (user['name'], user['picture'], user['company'], user['email'], user['phone'], user['country'], user['latitude'], user['longitude']))
#			print "a"
#		else:
#			print "2"
#			db.cursor().execute("""insert into users (name, picture, company, email, phone, latitude, longitude) values (?, ?, ?, ?, ?, ?, ?)""", (user['name'], user['picture'], user['company'], user['email'], user['phone'], user['latitude'], user['longitude']))
#			print "b"



#print getJSON("https://htn-interviews.firebaseio.com/users.json?download")[0]['country']
#populate("https://htn-interviews.firebaseio.com/users.json?download")
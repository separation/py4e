# Read roster_data.json and save in a database
# Sample code: https://www.py4e.com/code3/roster/roster.py
# Data: https://www.py4e.com/tools/sql-intro/roster_data.php?PHPSESSID=5ba1a426b9e5dd820f534439035f23eb

import json
import sqlite3

conn = sqlite3.connect('roaster.sqlite')
cur = conn.cursor()

cur.executescript('''
DROP TABLE IF EXISTS Course;
DROP TABLE IF EXISTS User;
DROP TABLE IF EXISTS Member;


CREATE TABLE Course(
	id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	title TEXT UNIQUE
);

CREATE TABLE User(
	id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	name TEXT UNIQUE
);

CREATE TABLE Member(
	user_id INTEGER,
	course_id	INTEGER,
	role INTEGER,
	PRIMARY KEY (user_id, course_id)
);
''')

with open('roster_data.json') as file:
	str_data = file.read()
	json_data = json.loads(str_data)

	for entry in json_data:
		user_name = entry[0]
		course_title = entry[1]
		role = entry[2]

		cur.execute('INSERT OR IGNORE INTO Course (title) VALUES (?)', (course_title,))
		cur.execute('SELECT id FROM Course WHERE title=?', (course_title,))
		course_id = cur.fetchone()[0]

		cur.execute('INSERT OR IGNORE INTO User (name) VALUES (?)', (user_name,))
		cur.execute('SELECT id FROM User WHERE name=?', (user_name,))
		user_id = cur.fetchone()[0]

		cur.execute('INSERT INTO Member (user_id, course_id, role) VALUES (?, ?, ?)', (user_id, course_id, role))
		conn.commit()


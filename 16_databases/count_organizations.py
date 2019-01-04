# Read the mailbox data (mbox.txt) and count the number of email messages
# per organization (i.e. domain name of the email address) using a database
# Sample: https://www.py4e.com/code3/emaildb.py
# Data: https://www.py4e.com/code3/mbox.txt

import sqlite3

def get_organizations(filename):
	with open(filename) as file:
		for line in file:
			if not line.startswith('From: '): continue
			words = line.split()
			email = words[1]
			org_pos = email.find('@')
			yield email[org_pos + 1:]


conn = sqlite3.connect('organizations.sqlite')
cur = conn.cursor()

cur.execute('DROP TABLE IF EXISTS Counts')
cur.execute('CREATE TABLE Counts (org TEXT, count INTEGER)')

for org in get_organizations('mbox.txt'):
	cur.execute('SELECT count FROM Counts WHERE org = ?', (org,))
	row = cur.fetchone()
	if row:
		cur.execute('UPDATE Counts SET count = count + 1 WHERE org = ?', (org,))
	else:
		cur.execute('INSERT INTO Counts (org, count) VALUES (?, 1)', (org,))

	conn.commit()

for row in cur.execute('SELECT org, count FROM Counts ORDER BY count DESC'):
	print(str(row[0]), row[1])



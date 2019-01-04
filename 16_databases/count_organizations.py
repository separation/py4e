# Read the mailbox data (mbox.txt) and count the number of email messages
# per organization (i.e. domain name of the email address) using a database
# Sample: https://www.py4e.com/code3/emaildb.py
# Data: https://www.py4e.com/code3/mbox.txt

import sqlite3

conn = sqlite3.connect('organizations.sqlite')
cur = conn.cursor()

cur.execute('DROP TABLE IF EXISTS Counts')
cur.execute('CREATE TABLE Counts (org TEXT, count INTEGER)')

with open('mbox.txt') as file:
	for line in file:
		if not line.startswith('From: '): continue
		words = line.split()
		email = words[1]
		pos = email.find('@')
		org = email[pos + 1:]

		cur.execute('SELECT count FROM Counts WHERE org = ?', (org,))
		row = cur.fetchone()
		if row:
			cur.execute('UPDATE Counts SET count = count + 1 WHERE org = ?', (org,))
		else:
			cur.execute('INSERT INTO Counts (org, count) VALUES (?, 1)', (org,))

		conn.commit()

for row in cur.execute('SELECT org, count FROM Counts ORDER BY count DESC'):
	print(str(row[0]), row[1])



# Parse the given Library.xml and store the musical tracks in a database
# Sample code and data: www.py4e.com/code3/tracks.zip

import xml.etree.ElementTree as ET
import sqlite3

def get_tracks(filename):
	with open(filename) as file:
		xml_parser = ET.parse(file)
		tracks_xml = xml_parser.findall('dict/dict/dict')
		for track_xml in tracks_xml:
			track_dict = {}
			for i, node in enumerate(track_xml):
				if node.tag == 'key':
					track_dict[node.text] = track_xml[i + 1].text
			yield track_dict


conn = sqlite3.connect('tracks.db')
cur = conn.cursor()

cur.executescript('''
DROP TABLE IF EXISTS Artist;
DROP TABLE IF EXISTS Album;
DROP TABLE IF EXISTS Genre;
DROP TABLE IF EXISTS Track;

CREATE TABLE Artist(
	id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	name TEXT UNIQUE
);

CREATE TABLE Album(
	id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	artist_id INTEGER,
	title TEXT UNIQUE
);

CREATE TABLE Genre(
	id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	name TEXT UNIQUE
);

CREATE TABLE Track(
	id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	title TEXT UNIQUE,
	album_id INTEGER,
	genre_id INTEGER,
	len INTEGER,
	rating INTEGER,
	count INTEGER
);
''')


for track in get_tracks('Library.xml'):
	name = track.get('Name')
	artist = track.get('Artist')
	album = track.get('Album')
	genre = track.get('Genre')
	count = track.get('Play Count')
	rating = track.get('Rating')
	length = track.get('Total Time')

	if not name or not artist or not album or not genre: continue

	# artist
	cur.execute('INSERT OR IGNORE INTO Artist (name) VALUES (?)', (artist,))
	cur.execute('SELECT id FROM Artist WHERE name=?', (artist,))
	artist_id = cur.fetchone()[0]

	# album
	cur.execute('INSERT OR IGNORE INTO Album (artist_id, title) VALUES (?, ?)', (artist_id, album))
	cur.execute('SELECT id FROM Album WHERE title=?', (album,))
	album_id = cur.fetchone()[0]

	# genre
	cur.execute('INSERT OR IGNORE INTO Genre (name) VALUES (?)', (genre,))
	cur.execute('SELECT id FROM Genre WHERE name=?', (genre,))
	genre_id = cur.fetchone()[0]

	# track
	cur.execute('''
		INSERT OR IGNORE INTO Track (title, album_id, genre_id, len, rating, count) 
		VALUES (?, ?, ?, ? , ?, ?)
		''', (name, album_id, genre_id, length, rating, count)
	)

	conn.commit()


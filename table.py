import sqlite3

conn = sqlite3.connect('tb.db')
print ("Opened database successfully")

conn.execute('CREATE TABLE users (username TEXT, email TEXT, password TEXT)')
print ("Table created successfully")
conn.close()
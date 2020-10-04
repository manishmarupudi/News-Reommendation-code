import sqlite3

conn = sqlite3.connect('news.db')
print("Opened database successfully")

conn.execute('''CREATE TABLE tags
         (ID INTEGER PRIMARY KEY    AUTOINCREMENT,
         EMAIL            		TEXT     NOT NULL,
         keyword            		TEXT     NOT NULL);''')
print ("Table created successfully")

conn.close()
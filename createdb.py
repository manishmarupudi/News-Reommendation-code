import sqlite3

conn = sqlite3.connect('news.db')
print("Opened database successfully")

conn.execute('''CREATE TABLE users
         (ID INTEGER PRIMARY KEY    AUTOINCREMENT,
         FIRST_NAME           	TEXT    NOT NULL,
         LAST_NAME           	TEXT    NOT NULL,
         EMAIL            		TEXT     NOT NULL,
         CONTACT        		CHAR(15),
         PASSWORD         		TEXT);''')
print ("Table created successfully")

conn.close()
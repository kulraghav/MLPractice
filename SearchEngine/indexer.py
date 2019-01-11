
"""
    index a link
"""

import sqlite3

conn = sqlite3.connect('test.db')

print("Opened database successfully.")

conn.execute("create table user (id int primary key not null, name text not null, age int not null);")

print("Table created successfully")

conn.execute("insert into user (id, name, age) values(111, 'OneOne', 11);")

cursor = conn.execute("select * from user where id=111;")

for row in cursor:
   print("ID = {}".format(row[0]))
   print("NAME = {}".format(row[1]))
   
conn.close()

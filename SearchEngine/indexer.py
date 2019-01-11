
"""
    index a link
"""

import sqlite3

con = sqlite3.connect('test.db')

print("Opened database successfully.")

def create_tables():
   con.execute('create table urllist(url)')
   con.execute('create table wordlist(word)')
   con.execute('create table wordlocation(urlid,wordid,location)')
   con.execute('create table link(fromid integer,toid integer)')
   con.execute('create table linkwords(wordid,linkid)')

   con.execute('create index on wordlist(word)')
   con.execute('create index on urllist(url)')
   con.execute('create index on wordlocation(wordid)')
   con.execute('create index urltoidx on link(toid)')
   con.execute('create index urlfromidx on link(fromid)')
   dbcommit( )            

def get_text(url):
   pass

def get_words(text):
   pass

def is_indexed(url):
   pass

def create_index(url):
   pass

conn.close()

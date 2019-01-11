
"""
    index a link
"""

import sqlite3
import requests
from bs4 import BeautifulSoup
import re

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

def get_text(url, soup=None):
   if not soup:
       page = requests.get(url)
       soup = BeautifulSoup(page.text, "html.parser")
   
   v =soup.string
   if v ==None:
       c=soup.contents
       
       resulttext=''
       for t in c:
           subtext= get_text(url, soup=t)
           resulttext+=subtext+'\n'
       return resulttext
   else:
       return v.strip( )

def get_words(text):
   splitter=re.compile('\\W*')
   return [s.lower( ) for s in splitter.split(text) if s!='']

def is_indexed(url):
   pass

def create_index(url):
   pass

con.close()

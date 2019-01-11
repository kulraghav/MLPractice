
"""
    index a link
"""

import sqlite3
import requests
from bs4 import BeautifulSoup
import re

con = sqlite3.connect('test.db')

print("Opened database successfully.")

ignorewords = []

def create_tables():
   con.execute('create table urllist(url)')
   con.execute('create table wordlist(word)')
   con.execute('create table wordlocation(urlid,wordid,location)')
   con.execute('create table link(fromid integer,toid integer)')
   con.execute('create table linkwords(wordid,linkid)')

   con.execute('create index wordidx on wordlist(word)')
   con.execute('create index urlidx on urllist(url)')
   con.execute('create index wordurlidx on wordlocation(wordid)')
   con.execute('create index urltoidx on link(toid)')
   con.execute('create index urlfromidx on link(fromid)')
   con.commit( )            

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
   u = con.execute("select rowid from urllist where url='%s'" % url).fetchone( )
   if u!=None:
   # Check if it has actually been crawled
       v = con.execute('select * from wordlocation where urlid=%d' % u[0]).fetchone( )
       if v!=None: return True
   return False
   
def create_index(url):
   if is_indexed(url):
      return

   print("Indexing {}".format(url))

   text = get_text(url)
   words = get_words(text)

   urlid = get_entry_id('urllist', 'url', url)

   # Link each word to this url
   for i in range(len(words)):
       word=words[i]
       if word in ignorewords: continue
       wordid= get_entry_id('wordlist','word',word)
       con.execute("insert into wordlocation(urlid,wordid,location) values (%d,%d,%d)" % (urlid,wordid,i))

   return

def get_entry_id(table,field,value,createnew=True):
    cur=con.execute("select rowid from %s where %s='%s'" % (table,field,value))
    res=cur.fetchone( )
    if res==None:
        cur = con.execute("insert into %s (%s) values ('%s')" % (table,field,value))
        return cur.lastrowid
    else:
        return res[0]
   

#con.close()

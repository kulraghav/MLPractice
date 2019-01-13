
import sqlite3

dbname = 'test.db'
con = sqlite3.connect(dbname)

def get_matches(query):
    # Strings to build the query
    fieldlist='w0.urlid'
    tablelist=''
    clauselist=''
    wordids=[]

    # Split the words by spaces
    words=query.split(' ')
    tablenumber=0

    for word in words:
        # Get the word ID
        wordrow= con.execute(
        "select rowid from wordlist where word='%s'" % word).fetchone( )
        if wordrow!=None:
            wordid=wordrow[0]
            wordids.append(wordid)
            if tablenumber>0:
                tablelist+=','
                clauselist+=' and '
                clauselist+='w%d.urlid=w%d.urlid and ' % (tablenumber-1,tablenumber)
                fieldlist+=',w%d.location' % tablenumber
                tablelist+='wordlocation w%d' % tablenumber
                clauselist+='w%d.wordid=%d' % (tablenumber,wordid)
                tablenumber+=1

    # Create the query from the separate parts
    fullquery = 'select {} from where {}'.format(fieldlist,tablelist,clauselist)
    print(fullquery)
    cur = con.execute(fullquery)
    rows = [row for row in cur]
    return rows,wordids            

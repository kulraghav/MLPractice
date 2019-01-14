"""
   issue con.execute returns None
"""


def get_matches_single(query, con):
    result = con.execute("select rowid from wordlist where word='{}'".format(query)).fetchone()
    return result

def get_matches_two(query, con):
    words = query.split(' ')

    l0 = con.execute("select rowid from wordlist where word='{}'".format(words[0])).fetchone()
    l1 = con.execute("select rowid from wordlist where word='{}'".format(words[1])).fetchone()

    print(l0, l1)
    q = "select w0.urlid,w0.location,w1.location from wordlocation w0,wordlocation w1 where w0.urlid=w1.urlid and w0.wordid={} and w1.wordid={}".format(l0, l1)

    cur = con.execute(q)

    return [row for row in cur]

def get_matches(query, con):
    # Strings to build the query
    fieldlist='w0.urlid'
    tablelist=''
    clauselist=''
    wordids=[]

    # Split the words by spaces
    words=query.split(' ')
    print(words)
    tablenumber=0

    for word in words:
        # Get the word ID
        wordrow= con.execute("select rowid from wordlist where word='{}'".format(word)).fetchone()
        print(wordrow)
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

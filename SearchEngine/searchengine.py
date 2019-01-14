
"""
    search engine test
"""

from indexer import create_tables, create_index
from crawler import crawl_and_index
from searcher import get_matches_single

import sqlite3

con = sqlite3.connect('test.db')
print("Connection successful!")

create_tables(con)

url = "http://kiwitobes.com/wiki/Categorical_list_of_programming_languages.html"
crawl_and_index([url], con)

print(get_matches_single("fire", con))




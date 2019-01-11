
import requests
from bs4 import BeautifulSoup

def is_valid(link):
    return True # test: is_valid function takes a lot of time

    try:
        requests.get(link)
        return True
    except:
        return False
    
def get_valid_links(base_url):
    try:
        page = requests.get(base_url)
        soup = BeautifulSoup(page.text, "html.parser")
        links = soup('a')
    except:
        print("Exception: requests.get({})".format(base_url))
        return []
        
    href_links = [link['href'] for link in links if 'href' in dict(link.attrs)]
    valid_links = [href_link for href_link in href_links if is_valid(href_link)]

    return valid_links

    
def crawl_and_index(base_urls, depth=2):
    indexed_urls = set()
    
    for i in range(depth):
        for base_url in base_urls:
            indexed_urls.add(base_url)
            links = get_valid_links(base_url)
            for link in links:
                if not link in indexed_urls:
                    indexed_urls.add(link)
                    
                    
    return indexed_urls         
            
        


import requests
from bs4 import BeautifulSoup

def get_links(base_url):
    page = requests.get(base_url)
    soup = BeautifulSoup(page.text, "html.parser")
    links = soup('a')
    return [link['href'] for link in links if 'href' in dict(link.attrs)]

    
def generate_urls(base_urls, depth=2):
    urls = set(base_urls)
    for i in range(depth):
        for base_url in base_urls:
            links = get_links(base_url)
            urls = urls.union(links)

    return urls         
            
        

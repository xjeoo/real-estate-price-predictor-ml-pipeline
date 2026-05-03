from bs4 import BeautifulSoup
import requests
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()
cwd = os.getcwd()

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept-Language': 'ro-RO,ro;q=0.9,en-US;q=0.8,en;q=0.7',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Referer': 'https://www.google.ro/'
}

xml_apartments_for_sale= os.getenv("XML_SITEMAP")

content = requests.get(xml_apartments_for_sale, headers=headers).text
soup = BeautifulSoup(content, 'xml')

urls = soup.find_all('url')

## PAGES TO SCRAPE
links = {
    "links": []
}
for url in urls:
    loc = url.find('loc')
    link = loc.text
    links["links"].append(link)

links_df = pd.DataFrame(links)
path = os.path.join(cwd, 'data', 'raw', 'sitemap_links.csv')
links_df.to_csv(path, index=False)


from bs4 import BeautifulSoup
import requests
import pandas as pd
import os
import time
import random
from dotenv import load_dotenv
from tqdm import tqdm # for progress bar

# O IDEE DE CE TREBUIE SCRAPEUIT:
# [ 
#   id, pret, zona, suprafata_utila, nr_camere, compartimentare?, an_constructie,
#   etaj, etaj_maxim?, numar_bai, parcare, url  
# ]
def scrape_page(link, headers): # returns object to be saved into df
    listing_id = link.split('-')[-1]

    content = requests.get(link, headers=headers).text
    soup = BeautifulSoup(content, 'html.parser')

    # price extraction start
    price_box_text = soup.find('div', attrs={
        "aria-label": "price"
    }).text.lower()
    price = "".join([c for c in price_box_text if c.isdigit()])
    currency = ""
    if "€" in price_box_text or "euro" in price_box_text or "eur" in price_box_text:
        currency = "euro"
    elif "ron" in price_box_text or "lei" in price_box_text:
        currency = "ron"
    else:
        currency = "euro"
    
    tva_included = False if "tva" in price_box_text and "inclus" not in price_box_text else True
    #price extraction end



    #------------------
    #build final object
    page_info = {
        "listing_id": listing_id,
        "price": price,
        "currency": currency,
        "tva_included": tva_included,
        "url": link
    }
    return page_info

#------- end of function definitions ------------------------------

cwd = os.getcwd()
links_csv_path = os.path.join(cwd, 'data', 'raw', 'sitemap_links.csv')
output_csv_path = os.path.join(cwd, 'data', 'raw', 'raw_listings.csv')
load_dotenv()

all_links_df = pd.read_csv(links_csv_path)
all_links = all_links_df["links"].to_list()
links_to_scrape = []
if os.path.exists(output_csv_path):
    print("Resuming scrape")
    output_df = pd.read_csv(output_csv_path)
    done_links = set(output_df["url"].to_list())
    links_to_scrape = [link for link in all_links if link not in done_links]
else:
    print("Starting from the beginning")
    links_to_scrape = all_links

referer = os.getenv("REFERER")
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept-Language': 'ro-RO,ro;q=0.9,en-US;q=0.8,en;q=0.7',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Referer': referer
}
try:
    # main loop
    for link in tqdm(links_to_scrape[:6]):
        try:    
            time.sleep(random.uniform(2.2, 4.1))
            row = scrape_page(link, headers)
            row_df = pd.DataFrame([row])
            row_df.to_csv(output_csv_path, mode='a', index=False, header= not os.path.exists(output_csv_path))

        except Exception as err:
            print("Scraping failed at link: ", link)
            print("Error details: ", err)

except KeyboardInterrupt:
    print("\n<Script interrupted>")


print("Scraping done")
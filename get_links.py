from bs4 import BeautifulSoup
import requests
import pandas as pd
import os
from dotenv import load_dotenv


def fetch_sitemap_links(sitemap_url: str, headers: dict) -> list:
    """Extract and return all URLs from the XML sitemap."""
    content = requests.get(sitemap_url, headers=headers).text
    soup = BeautifulSoup(content, 'xml')

    urls = soup.find_all('url')

    links = []
    for url in urls:
        loc = url.find('loc')
        link = loc.text
        links.append(link)

    return links


# ==========================================
#  MAIN FUNCTION
# ==========================================
def run_link_scraper(output_path: str):
    """Orchestrate loading environment variables, extraction, and saving to CSV."""
    load_dotenv()

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept-Language': 'ro-RO,ro;q=0.9,en-US;q=0.8,en;q=0.7',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Referer': 'https://www.google.ro/'
    }

    sitemap_url = os.getenv("XML_SITEMAP")

    links = fetch_sitemap_links(sitemap_url, headers)

    links_df = pd.DataFrame({"links": links})
    links_df.to_csv(output_path, index=False)

# ==========================================
# ENTRY POINT
# ==========================================

if __name__ == "__main__":
    OUTPUT_FILE = os.path.join(os.getcwd(), 'data', 'raw', 'sitemap_links.csv')
    run_link_scraper(OUTPUT_FILE)
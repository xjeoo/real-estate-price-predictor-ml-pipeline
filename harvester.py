from bs4 import BeautifulSoup
import pandas as pd
import os
import time
import random
from tqdm import tqdm # for progress bar
from utils.scrape_utils import get_basic_details, get_price_info, get_location_info, get_specifications
from utils.session_utils import get_new_session


def scrape_page(link, session): # returns object to be saved into df
    listing_id = link.split('-')[-1]

    content = session.get(link, timeout=30).text
    soup = BeautifulSoup(content, 'html.parser')
    
    #price info
    price, currency, tva_included = get_price_info(soup)
    #basic details
    numar_camere, supraf_util, etaj, etaj_max, an_constr, an_constr_status = get_basic_details(soup)
    #location info
    sector, neighbourhood, distance_to_subway_m = get_location_info(soup)
    # other specs
    layout, number_of_bathrooms, comfort_grade, has_balcony, parking_spots, heating_type = get_specifications(soup)


    #------------------
    #build final object
    page_info = {
        "listing_id": listing_id,
        "price": price,
        "currency": currency,
        "tva_included": tva_included,
        "sector": sector,
        "neighbourhood": neighbourhood,
        "distance_to_subway_meters": distance_to_subway_m,
        "nr_of_rooms": numar_camere,
        "usable_surface_sq_meters": supraf_util,
        "floor": etaj,
        "max_floor": etaj_max,
        "construction year": an_constr,
        "construction_status": an_constr_status,
        "layout": layout,
        "number_of_bathrooms": number_of_bathrooms,
        "comfort_grade": comfort_grade,
        "has_balcony": has_balcony,
        "parking_spots": parking_spots,
        "heating_type": heating_type,
        "url": link
    }
    return page_info



# ==========================================
# MAIN FUNCTION
# ==========================================

def run_harvester(links_csv_path: str, output_csv_path: str, failed_link_csv_path: str):
    """Manage the link queue, session rotation, and incremental saving."""

    all_links_df = pd.read_csv(links_csv_path)
    all_links = all_links_df["links"].to_list()

    failed_links_set = set()
    if os.path.exists(failed_link_csv_path):
        failed_link_df = pd.read_csv(failed_link_csv_path)
        failed_links = failed_link_df["link"].to_list()
        failed_links_set = set(failed_links)
    links_to_scrape = []
    if os.path.exists(output_csv_path):
        print("Resuming scrape")
        output_df = pd.read_csv(output_csv_path)
        done_links = set(output_df["url"].to_list())
        links_to_scrape = [link for link in all_links if link not in done_links and link not in failed_links_set]
    else:
        print("Starting from the beginning")
        links_to_scrape = all_links


    try:
        # main loop
        current_session = get_new_session() # create first session
        for idx, link in enumerate(tqdm(links_to_scrape)):
            if idx > 0 and idx % 150 == 0:
                current_session.close() # close old connection
                print("-Rotating session at index", idx, ". Pausing 10 seconds.")
                time.sleep(random.uniform(8.0, 15.0)) # bigger pause
                current_session = get_new_session()
            
            try:    
                time.sleep(random.uniform(2.2, 4.1))
                row = scrape_page(link, current_session)
                row_df = pd.DataFrame([row])
                row_df.to_csv(output_csv_path, mode='a', index=False, header= not os.path.exists(output_csv_path))

            except Exception as err:
                print("Scraping failed at link: ", link)
                print("Adding link to failed links.")
                print("Error details: ", err)
                failed_link = {
                    "link": link,
                    "error_details": str(err)
                }
                failed_link_df = pd.DataFrame([failed_link])
                failed_link_df.to_csv(failed_link_csv_path, mode='a', index=False, header= not os.path.exists(failed_link_csv_path))

    except KeyboardInterrupt:
        print("\n<Script interrupted>")

    finally:
        if 'current_session' in locals(): # closing last session
            current_session.close()

    print("Scraping done")

# ==========================================
# ENTRY POINT
# ==========================================

if __name__ == "__main__":
    cwd = os.getcwd()
    LINKS_PATH = os.path.join(cwd, 'data', 'raw', 'sitemap_links.csv')
    OUTPUT_PATH = os.path.join(cwd, 'data', 'raw', 'raw_listings.csv')
    FAILED_PATH = os.path.join(cwd, 'data', 'raw', 'failed_links.csv')

    print("Starting scraping process...")
    run_harvester(LINKS_PATH, OUTPUT_PATH, FAILED_PATH)

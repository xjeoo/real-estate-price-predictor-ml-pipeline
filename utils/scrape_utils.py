from bs4 import BeautifulSoup

def safe_extract(label_element): # used for basic_details_labels
    if label_element:
        return label_element.find_next('span').find_next('span').text
    return "None"

def get_price_info(soup: BeautifulSoup):
    """
    Returns [price, currency, tva_included] from a BeautifulSoup soup
    """
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

    return [price, currency, tva_included]

def get_basic_details(soup: BeautifulSoup):

    """
    Returns a [numar_camere, supraf_util, etaj, etaj_max, an_constr, constr_status] from a BeautifulSoup soup
    """

    basic_details = soup.find('div', attrs={
        "data-cy": "listing-basic-details-list"
    })
    # ------- number of rooms
    numar_camere_label = basic_details.find('span', string=lambda text: text and "Nr. cam" in text )
    numar_camere = safe_extract(numar_camere_label)
    # ------- usable square area 
    supraf_util_label = basic_details.find('span', string=lambda text: text and "Sup. util" in text )
    supraf_util = safe_extract(supraf_util_label).split(' ')[0].replace(',','.')
    # ------- floor and max_floor
    etaj_label = basic_details.find('span', string=lambda text: text and "Etaj" in text )
    etaj = safe_extract(etaj_label).replace(' ','')
    etaj_max = "None"
    if '/' in etaj:
        etaj_string = etaj.split('/')
        etaj = etaj_string[0]
        etaj_max = etaj_string[1]
    # ------- construction year
    an_constr_label = basic_details.find('span', string=lambda text: text and "An constr" in text )
    an_constr_text = safe_extract(an_constr_label)
    an_constr = an_constr_text
    an_constr_status = "None"
    if '(' in an_constr_text:
        an_constr_string = an_constr_text.split('(')
        an_constr = an_constr_string[0].strip()
        an_constr_status = an_constr_string[1].replace(')', '')

    basic_details_output = [numar_camere, supraf_util, etaj, etaj_max, an_constr, an_constr_status]

    return basic_details_output



def get_location_info(soup: BeautifulSoup):
    """
    Returns [sector, neighbourhood, distance_to_subway_m ] from a BeautifulSoup soup
    """
    breadcrumbs_elements = soup.find('nav', attrs={
        "data-cy": "breadcrumbs"
    }).find_all('li')

    # if not breadcrumbs_elements return [ "None" * 6]
    if 'Sector' in breadcrumbs_elements[4].text.strip():
        sector = breadcrumbs_elements[4].text.strip().split(' ')[1]
    else:
        sector = breadcrumbs_elements[4].text.strip() # ultracentral - will be mapped to 0
    neighbourhood = breadcrumbs_elements[5].text.strip()

    points_of_interest_header = soup.find('h2', string=lambda text: text and "Puncte de interes" in text)
    if points_of_interest_header:
        points_of_interest_section = points_of_interest_header.find_parent('section')
        subway_span = points_of_interest_section.find("span", string=lambda text: text and "metrou" in text)
        distance_to_subway_m = None
        if subway_span :
            distance_to_subway_text = subway_span.find_next('span').text
            if distance_to_subway_text:
                distance_to_subway_m = "".join([c for c in distance_to_subway_text if c.isdigit()])
    return [sector, neighbourhood, distance_to_subway_m]


def get_specifications(soup: BeautifulSoup):
    """
    Returns [ ... ] from a BeautifulSoup soup
    """
    #layout
    layout = None
    layout_span = soup.find("span", attrs={
                                "class": "text-md border-soft rounded-full border bg-white px-3 py-1 text-gray-700"
                            },
                            string=lambda text: text and 
                            ("comandat" in text.lower() or "circular" in text.lower() or "vagon" in text.lower())
                            )
    if layout_span:
        layout = layout_span.text.strip().lower()

    # number_of_bathrooms
    number_of_bathrooms = 1
    number_of_bathrooms_elem = soup.find('span', string=lambda text: text and "Nr. băi" in text)
    if number_of_bathrooms_elem:
        number_of_bathrooms_next = number_of_bathrooms_elem.find_next('span')
        if number_of_bathrooms_next:
            number_of_bathrooms = number_of_bathrooms_next.text.strip()

    # comfort_grade
    comfort_grade_elem = soup.find('span', attrs={
                                    "class": "text-md border-soft rounded-full border bg-white px-3 py-1 text-gray-700"
                                    },
                                    string=lambda text: text and "Confort" in text)
    comfort_grade = None
    if comfort_grade_elem:
        comfort_grade = comfort_grade_elem.text.replace("Confort", '').strip()

    # has_balcony
    balcony_elem = soup.find("span", attrs={
                                "class": "text-md border-soft rounded-full border bg-white px-3 py-1 text-gray-700"
                            }, string=lambda text: text and 
                            ("balcon" in text.lower() or "balcoane" in text.lower() or "teras" in text.lower())
                            )
    has_balcony = True if balcony_elem else False
    if not has_balcony:
        description_elem = soup.find("div", attrs={
            "data-cy": "listing-description-section"
        })
        description = description_elem.text.lower() if description_elem else ""
        has_balcony = "balcon" in description or "balcoane" in description or "teras" in description # terasa

    # parking_spots
    parking_spots = 0
    parking_spot_span = soup.find("span", attrs={
                                    "class": "text-md border-soft rounded-full border bg-white px-3 py-1 text-gray-700"
                                },
                                string=lambda text: text and 
                                ("parcare" in text.lower() or "parcări" in text.lower() or "parcari" in text.lower()))
    if parking_spot_span:
        parking_spots = "".join([c for c in parking_spot_span.text if c.isdigit()])
        if parking_spots == "":
            parking_spots = 1
        else:
            parking_spots = int(parking_spots)

    # heating_type
    heating_type = None
    heating_span = soup.find("span", attrs={
                                "class": "text-md border-soft rounded-full border bg-white px-3 py-1 text-gray-700"
                            },
                              string=lambda text: text and 
                            ("centrală" in text.lower() or "centrala" in text.lower())
                            )
    if heating_span:
        heating_type = heating_span.text.strip().lower()

    return [layout, number_of_bathrooms, comfort_grade, has_balcony, parking_spots, heating_type]

    
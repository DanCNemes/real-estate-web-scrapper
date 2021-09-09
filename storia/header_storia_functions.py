import re
from datetime import date, timedelta
from db_objects import db

header_keys = ['header_id', 'num_of_rooms', 'surface', 'compartment', 'floor', 'construction_year', 'property_type',
               'parking_space', 'balcony', 'location', 'price', 'source', 'seller_type', 'header_date']

today = date.today()

db_session = db.DbRealEstate()


def get_headers_page_urls(soup_obj):
    header_page_urls_list = []
    for header_elem in soup_obj.find_all("article"):
        if header_elem is not None:
            if not db_session.header_id_exists(header_elem.get("data-tracking-id")):
                header_page_urls_list.append(header_elem.get("data-url"))
            else:
                print("Header already exists")

    return header_page_urls_list


def get_header_info(header_page_soup):
    header_information = dict.fromkeys(header_keys)

    get_header_id(header_page_soup, header_information)
    get_header_price(header_page_soup, header_information)
    get_header_location(header_page_soup, header_information)
    get_header_source(header_information)
    get_header_surface(header_page_soup, header_information)
    get_header_rooms(header_page_soup, header_information)
    get_header_compartment(header_page_soup, header_information)
    get_header_construction_year(header_page_soup, header_information)
    get_header_floor(header_page_soup, header_information)
    get_header_property_type(header_page_soup, header_information)
    get_header_features(header_page_soup, header_information)
    get_header_seller_type(header_page_soup, header_information)
    get_header_date(header_page_soup, header_information)

    return header_information


def get_header_price(header_page_soup, header_dict):
    price_strong = header_page_soup.find("strong", {"data-cy": "adPageHeaderPrice"})

    if price_strong is not None:
        header_dict['price'] = price_strong.text


def get_header_location(header_page_soup, header_dict):
    location_tag = header_page_soup.find("a", {"class": "css-1i2ocqu e1nbpvi63"})

    if location_tag is not None:
        header_dict['location'] = location_tag.text


def get_header_surface(header_page_soup, header_dict):
    div_tag = header_page_soup.find("div", {"aria-label": "Suprafata utila (m²)"})
    if div_tag is not None:
        div_surface = div_tag.find("div", {"class": "css-1ytkscc ev4i3ak0"})
        if div_surface is not None:
            header_dict['surface'] = div_surface.text


def get_header_rooms(header_page_soup, header_dict):
    div_tag = header_page_soup.find("div", {"aria-label": "Numarul de camere"})
    if div_tag is not None:
        div_rooms = div_tag.find("div", {"class": "css-1ytkscc ev4i3ak0"})
        if div_rooms is not None:
            header_dict['num_of_rooms'] = div_rooms.text


def get_header_compartment(header_page_soup, header_dict):
    div_tag = header_page_soup.find("div", {"aria-label": "Compartimentare"})
    if div_tag is not None:
        div_compartment = div_tag.find("div", {"class": "css-1ytkscc ev4i3ak0"})
        if div_compartment is not None:
            header_dict['compartment'] = div_compartment.text


def get_header_construction_year(header_page_soup, header_dict):
    div_tag = header_page_soup.find("div", {"aria-label": "Anul constructiei"})
    if div_tag is not None:
        div_construction_year = div_tag.find("div", {"class": "css-1ytkscc ev4i3ak0"})
        if div_construction_year is not None:
            header_dict['construction_year'] = div_construction_year.text


def get_header_floor(header_page_soup, header_dict):
    div_tag = header_page_soup.find("div", {"aria-label": "Etaj"})
    if div_tag is not None:
        div_floor = div_tag.find("div", {"class": "css-1ytkscc ev4i3ak0"})
        if div_floor is not None:
            header_dict['floor'] = div_floor.text


def get_header_property_type(header_page_soup, header_dict):
    div_tag = header_page_soup.find("div", {"aria-label": "Tip proprietate"})
    if div_tag is not None:
        div_property_type = div_tag.find("div", {"class": "css-1ytkscc ev4i3ak0"})
        if div_property_type is not None:
            header_dict['property_type'] = div_property_type.text


def get_header_features(header_page_soup, header_dict):
    features = header_page_soup.find_all("li", {"data-cy": "ad.ad-features.categorized-list.item-with-category"})

    if features is not None:
        for feature in features:
            if "balcon" in str(feature.text):
                header_dict['balcony'] = 'Da'
            elif "parcare" in str(feature.text):  
                header_dict['parking_space'] = 'Da'


def get_header_source(header_dict):
    header_dict['source'] = 'www.storia.ro'


def get_header_id(header_page_soup, header_dict):
    div_tag = header_page_soup.find("div", {"class": "css-jjerc6 euuef474"})

    if div_tag is not None:
        div_contents = div_tag.text
    else:
        div_contents = ''

    id_regex = "\d\d\d\d\d\d\d"
    match = re.search(id_regex, str(div_contents))
    if match:
        header_dict['header_id'] = match.group(0)


def get_header_seller_type(header_page_soup, header_dict):
    seller_type_div = header_page_soup.find("div", {"class": "css-xmh88c ecc3f2c0"})

    if seller_type_div is not None:
        seller_type = seller_type_div.find("span")
        header_dict['seller_type'] = seller_type.text
    else:
        header_dict['seller_type'] = None


def get_header_date(header_page_soup, header_dict):
    date_tag = header_page_soup.find("div", {"class": "css-3jrcf7 euuef471"})
    num_of_days_regex = "\d+"

    if date_tag is not None:
        match = re.search(num_of_days_regex, str(date_tag.text))
        if match is not None:
            header_date = today - timedelta(days=int(match.group()))
            header_date = header_date.strftime("%d.%m.%Y")

            header_dict['header_date'] = header_date
    else:
        header_dict['header_date'] = today.strftime("%d.%m.%Y")

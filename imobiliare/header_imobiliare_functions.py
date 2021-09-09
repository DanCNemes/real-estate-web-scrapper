import re
import unidecode
from datetime import date, timedelta
from db_objects import db

header_keys = ['header_id', 'num_of_rooms', 'surface', 'compartment', 'floor', 'construction_year', 'property_type',
               'parking_space', 'balcony', 'location', 'price', 'source', 'seller_type', 'header_date']

today_string = date.today().strftime("%d.%m.%Y")
yesterday_date = date.today() - timedelta(days=1)
yesterday_string = yesterday_date.strftime("%d.%m.%Y")

db_session = db.DbRealEstate()


def get_headers_page_urls(base_url, soup_obj):
    header_page_urls_list = []
    for header_elem in soup_obj.find_all("div", {"class": "box-anunt"}):
        header_id = header_elem.get('id')
        if header_id:
            if not db_session.header_id_exists(header_id):
                header_page_urls_list.append(base_url + header_id)
            else:
                print('Header exists')

    return header_page_urls_list


def get_header_info(header_page_soup):
    header_information = dict.fromkeys(header_keys)

    get_header_price(header_page_soup, header_information)
    get_header_location(header_page_soup, header_information)
    get_header_details_ul_list(header_page_soup, header_information)
    get_header_details_ul_mobile_list(header_page_soup, header_information)
    get_header_source(header_information)
    get_header_id(header_page_soup, header_information)
    get_header_seller_type(header_page_soup, header_information)
    get_header_date(header_page_soup, header_information)

    return header_information


def get_header_price(header_page_soup, header_dict):
    price_div = header_page_soup.find("div", {"itemprop": "price"})
    price_value = None
    price_currency_value = None
    if price_div is not None:
        price_value = price_div.find("span")
        price_currency_div = price_div.find("div")
        price_currency_value = price_currency_div.find("p")

    header_dict['price'] = unidecode.unidecode(str(price_value.text) + str(price_currency_value.text))


def get_header_location(header_page_soup, header_dict):
    location = header_page_soup.find("div", {"class": "col-lg-9 col-md-9 col-sm-9 col-xs-12"})

    header_dict['location'] = unidecode.unidecode(location.text)


def get_header_details_ul_list(header_page_soup, header_dict):
    ul_tag = header_page_soup.find("ul", {"class": "lista-tabelara"})
    li_tags = ul_tag.find_all("li")
    for li_tag in li_tags:
        if "Nr. camere:" in str(li_tag.text):
            header_dict['num_of_rooms'] = li_tag.find("span").text
        if "Suprafata utila:" in unidecode.unidecode(str(li_tag.text)):
            header_dict['surface'] = li_tag.find("span").text
        if "Compartimentare:" in str(li_tag.text):
            header_dict['compartment'] = li_tag.find("span").text
        if "Etaj:" in str(li_tag.text):
            header_dict['floor'] = li_tag.find("span").text


def get_header_details_ul_mobile_list(header_page_soup, header_dict):
    ul_tag = header_page_soup.find("ul", {"class": "lista-tabelara mobile-list"})
    li_tags = ul_tag.find_all("li")
    for li_tag in li_tags:
        if "An constructie:" in unidecode.unidecode(str(li_tag.text)):
            header_dict['construction_year'] = li_tag.find("span").text
        if "Tip imobil:" in str(li_tag.text):
            header_dict['property_type'] = li_tag.find("span").text
        if "locuri parcare:" in unidecode.unidecode(str(li_tag.text)):
            header_dict['parking_space'] = 'Da'
        if "Nr. balcoane:" in unidecode.unidecode(str(li_tag.text)):
            header_dict['balcony'] = 'Da'


def get_header_source(header_dict):
    header_dict['source'] = 'www.imobiliare.ro'


def get_header_id(header_page_soup, header_dict):
    li_tag = header_page_soup.find("li", {"class": "identificator-oferta"})
    li_tag_text = li_tag.text
    header_id = 'anunt-' + li_tag_text

    header_dict['header_id'] = header_id


def get_header_seller_type(header_page_soup, header_dict):
    seller_type = None
    key_word = 'sSellerType'
    script_tags = header_page_soup.find_all("script")
    script_data = str(script_tags[7].contents)
    script_elements = script_data.split(',')
    for item in script_elements:
        item.strip()
        item.rstrip()
        if key_word in item:
            seller_type = item.split("'sSellerType': ", 1)[1].replace("'", "")

    header_dict['seller_type'] = seller_type


def get_header_date(header_page_soup, header_dict):
    date_tag = header_page_soup.find("span", {"class": "data-actualizare"})
    date_regex = "\d\d\.\d\d\.\d\d\d\d"
    match = re.search(date_regex, str(date_tag.contents))

    if match:
        header_dict['header_date'] = match.group(0)
    elif 'ieri' in str(date_tag.contents).lower():
        header_dict['header_date'] = yesterday_string
    elif 'astazi' in str(date_tag.contents).lower():
        header_dict['header_date'] = today_string



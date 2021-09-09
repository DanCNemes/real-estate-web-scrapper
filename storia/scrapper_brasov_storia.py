from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time
import sys
sys.path.append('/home/dan/PycharmProjects/DissertationProject/storia')
sys.path.append('/home/dan/PycharmProjects/DissertationProject')
from storia import header_storia_functions
from helper_functions import insert_headers_to_csv


headers = []


def main():

    try:
        base_url = 'https://www.storia.ro/inchiriere/apartament/brasov/brasov/'

        # Instantiate webdriver using headless Chrome browser
        options = Options()
        options.headless = True
        dr = webdriver.Chrome(ChromeDriverManager().install(), options=options)

        # Get main page of website
        dr.get(base_url)
        main_source = dr.page_source
        main_soup = BeautifulSoup(main_source, "html.parser")

        last_page = get_last_page(main_soup)

        for page_number in range(1, last_page + 1):
            # Loop until last page and get header URL's
            base_crawl_url = 'https://www.storia.ro/inchiriere/apartament/brasov/brasov/?page='
            next_page_url = base_crawl_url + str(page_number)
            dr.get(next_page_url)
            next_source = dr.page_source
            next_soup = BeautifulSoup(next_source, "html.parser")
            next_header_page_urls = header_storia_functions.get_headers_page_urls(next_soup)
            for header_page_url in next_header_page_urls:
                # Loop through headers and get required information from header as dict
                dr.get(header_page_url)
                header_source = dr.page_source
                header_soup = BeautifulSoup(header_source, "html.parser")
                header_dict = header_storia_functions.get_header_info(header_soup)
                headers.append(header_dict)
                print(header_dict)
                time.sleep(0.5)

        insert_headers_to_csv("/home/dan/PycharmProjects/DissertationProject/csv_files/",
                              "brasov_storia.csv", headers)
    except Exception as e:
        insert_headers_to_csv("/home/dan/PycharmProjects/DissertationProject/csv_files/",
                              "brasov_storia.csv", headers)
        print("Scrapper failed: " + str(e))


def get_last_page(soup_obj):
    ul_tag = soup_obj.find("ul", {"class": "pager"})
    li_tags = ul_tag.find_all("li")
    last_page_li_tag = li_tags[4]
    last_page_a_tag = last_page_li_tag.find("a")
    last_page = last_page_a_tag.text

    return int(last_page)


main()

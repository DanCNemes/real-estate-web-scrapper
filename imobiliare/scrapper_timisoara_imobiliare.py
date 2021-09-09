import sys
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time

sys.path.append('/home/dan/PycharmProjects/DissertationProject/imobiliare')
sys.path.append('/home/dan/PycharmProjects/DissertationProject')
from imobiliare import header_imobiliare_functions
from helper_functions import insert_headers_to_csv

headers = []


def main():
    try:

        base_url = 'https://www.imobiliare.ro/inchirieri-apartamente/timisoara/'

        # Instantiate webdriver using headless Chrome broswer
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
            base_crawl_url = 'https://www.imobiliare.ro/inchirieri-apartamente/timisoara?pagina='
            next_page_url = base_crawl_url + str(page_number)
            dr.get(next_page_url)
            next_source = dr.page_source
            next_soup = BeautifulSoup(next_source, "html.parser")
            next_header_page_urls = header_imobiliare_functions.get_headers_page_urls(base_url, next_soup)
            for header_page_url in next_header_page_urls:
                # Loop through headers and get required information from header as dict
                dr.get(header_page_url)
                header_source = dr.page_source
                header_soup = BeautifulSoup(header_source, "html.parser")
                header_dict = header_imobiliare_functions.get_header_info(header_soup)
                headers.append(header_dict)
                print(header_dict)
                time.sleep(0.5)

        insert_headers_to_csv("/home/dan/PycharmProjects/DissertationProject/csv_files/",
                              "timisoara_imobiliare.csv", headers)

    except:
        insert_headers_to_csv("/home/dan/PycharmProjects/DissertationProject/csv_files/",
                              "timisoara_imobiliare.csv", headers)
        print("Exception occured")


def get_last_page(soup_obj):
    pages_tag = soup_obj.find_all("a", {"class": "butonpaginare"})
    last_page_tag = pages_tag[-2].contents
    page_num = int(last_page_tag[0])

    return page_num


main()

import requests
from bs4 import BeautifulSoup
import time
import pandas as pd
import yaml
from src import logging_manager as log

with open('config/config.yml') as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}


# getting all products links from the main page. For current category there are 9 pages
productslinks = []
def get_links():
    for x in range(1, config['num_of_pages_to_scrape']):
        url = f'https://50style.lt/vyrams/avalyne?page={x}'
        r = requests.get(url, headers=headers)
        soup = BeautifulSoup(r.content, 'html.parser')
        productslist = soup.find_all('div', {'class': 'b-itemList_desc'})
        for item in productslist:
            link = 'https://50style.lt' + item.find('a')['href']
            productslinks.append(link)
            log.o_info(f'Products link\'s list appended: {link}')


#getting a certain product details
product_data = []
def get_product_info():
    for link in productslinks:
        r = requests.get(link, headers=headers)
        soup = BeautifulSoup(r.content, 'html.parser')
        try:
            productId = soup.find('span', {'class': 'm-accordion_productCode'}).text.strip()
            name = soup.find('h1', {'class': 'm-productDescr_headline js-offerTooltip_call'}).text.strip()
            price = soup.find('span', {'class': 'price-value'}).text.strip()
            available = soup.find('p', {'class': 'product-information'}).text.strip()
            link = link
            log.o_info(f'Product {name} info saved successfully!')
        except:
            productId = None
            name = None
            price = None
            available = None
            link = link
            log.o_info('Product don\'t have full info! Check link manually!')
        product = {
            'productId': productId,
            'name': name,
            'price': price,
            'available': available,
            'link': link
        }
        product_data.append(product)
        print('Saving: ', product['name'])
        time.sleep(config['time_to_sleep'])


#saving scraped data to file
def save_info():
    if len(product_data) > 0:
        df = pd.DataFrame(product_data)
        try:
            if config['format_for_saving'] == 'xlsx':
                df.to_excel('fiftystyle.xlsx', index=False)
                log.o_info('Scraping completed! Data saved to XLSX file!')
                print('Scraping completed! Data saved to XLSX file!')
            elif config['format_for_saving'] == 'csv':
                df.to_csv('fiftystyle.csv')
                log.o_info('Scraping completed! Data saved to CSV file!')
                print('Scraping completed! Data saved to CSV file!')
        except Exception as e:
            print(e)
            log.o_info(e)
    else:
        log.o_info('There is no data to save!')
        print('There is no data to save!')
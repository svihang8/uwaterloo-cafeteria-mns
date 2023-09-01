import os
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from urllib import request
from itertools import chain
from datetime import datetime
from MenuScraper.Dish import Dish
import pandas as pd

class Scraper():

    load_dotenv()
    BASE_URL = os.getenv('BASE_URL')
    ITEM_BASE_URL = os.getenv('ITEM_BASE_URL')

    def __init__(self, date = datetime.today().strftime('%Y-%m-%d')) -> None:
        self.date = date
        self.items = []
        self._download_menu()

    def _download_menu(self):
        download_url = self.BASE_URL + str(self.date)
        page_bytes = request.urlopen(download_url)
        soup = BeautifulSoup(page_bytes, 'html.parser')
        menu_nodes = soup.find_all('ul', attrs={'class' : 'dm-menus'})
        for menu_node in menu_nodes:
            item_nodes = (menu_node.find_all('a'))
            for item_node in item_nodes:
                item_url = item_node['href']
                item_url = self.ITEM_BASE_URL + item_url
                item_name = item_node.get_text()
                dish = Dish(item_url, item_name)
                self.items.append(dish.dish)
    
    def _get_data(self) -> pd.DataFrame:
        data = []
        for item in self.items:
            for ingredient in item[3]:
                data.append([self.date, item[0], item[1], item[2], ingredient, False])
            for allergen in item[4]:
                data.append([self.date, item[0], item[1], item[2], allergen, True])
        df = pd.DataFrame(data=data, columns=['date', 'name', 'url', 'serving_size', 'ingredient', 'allergen'])
        return df

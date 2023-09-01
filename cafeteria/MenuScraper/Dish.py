from bs4 import BeautifulSoup
from urllib import request
from itertools import chain
from datetime import datetime
import itertools
import re

class Dish():

    def __init__(self, url, name) -> None:
        self.url = url
        self.name = name
        self.page = self._download_info()
        self.serving_size = self._extract_serving_size()
        self.ingredients = self._extract_ingredients()
        self.allergens = self._extract_allergens()
        self.dish = [self.name, self.url, self.serving_size, self.ingredients, self.allergens]
    def _download_info(self):
        download_url = self.url
        page_bytes = request.urlopen(download_url)
        soup = BeautifulSoup(page_bytes, 'html.parser')
        return soup
    
    def _extract_serving_size(self):
        try:
            soup = self.page
            serving_size_node = soup.find('div', attrs={'class' : 'field-name-field-serving-size'})
            serving_size = serving_size_node.findAll('div', attrs={'class' : 'field-item'})[0]
            serving_size = serving_size.get_text()
            return serving_size
        except:
            return -1
    
    def _extract_ingredients(self):
        try:
            soup = self.page
            ingredients_node = soup.find('div',attrs={'class' : 'field-name-field-ingredients'})
            ingredients = ingredients_node.findAll('div', attrs={'class' : 'field-item'})
            rarr = []
            str = ingredients[0].get_text()
            rarr = re.split(',\s*(?![^()]*\))', str)
            rarr = [ingredient.strip().lower()[:255] for ingredient in rarr]
            if not rarr:
                return []
            return rarr
        except:
            print('exception')
            return []
    
    def _extract_allergens(self):
        try:
            soup = self.page
            allergens_node = soup.find('div',attrs={'class' : 'field-name-field-allergens'})
            allergens = allergens_node.findAll('div', attrs={'class' : 'field-item'})
            rarr = []
            for allergen in allergens:
                str = allergen.get_text()
                str = str.replace('May contain', '')
                str = str.replace('Contains', '')
                rarr.append(str.strip().lower())
            return rarr
        except:
            return []



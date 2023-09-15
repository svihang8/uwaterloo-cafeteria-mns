import os
from bs4 import BeautifulSoup
from urllib import request
from itertools import chain
from datetime import datetime, timedelta
import pandas as pd
import itertools
import re
import os
import mysql.connector
import sys

class Scraper():
    BASE_URL = os.environ['BASE_URL']
    ITEM_BASE_URL = os.environ['ITEM_BASE_URL']

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

class Database:
   db = mysql.connector.connect(
      host = os.environ['DATABASE_HOST'],
      user=os.environ['DATABASE_USER'],
      password=os.environ['DATABASE_PASSWORD'],
      database=os.environ['DATABASE_DATABASE']
   )
   cursor = db.cursor()

   def __init__(self, df = pd.DataFrame()):
      self.df = df
      print(self.db)
   
   def _handle_data(self):
      dish_df = self.df[['name', 'url']].drop_duplicates().reset_index()
      self._update_dishes(dish_df)
      ingredient_df = self.df[['ingredient', 'allergen']].drop_duplicates().reset_index()
      self._update_ingredients(ingredient_df)
      menu_df = self.df[['date', 'name']].drop_duplicates().reset_index()
      self._update_menu(menu_df)
      dishingredient_df = self.df[['name', 'ingredient']].drop_duplicates().reset_index()
      self._update_dishingredient(dishingredient_df)
   
   def _update_dishes(self, df):
      #sql = "DROP TABLE Dishes"
      #self.cursor.execute(sql)
      sql = "CREATE TABLE IF NOT EXISTS Dishes(id INT PRIMARY KEY AUTO_INCREMENT, dish VARCHAR(255) UNIQUE NOT NULL , url text)"
      self.cursor.execute(sql)
      for i in range(len(df)):
         sql = "INSERT IGNORE INTO Dishes (dish, url) VALUES (%s, %s)"
         val = (df.loc[i, 'name'], df.loc[i, 'url'])
         self.cursor.execute(sql, val)
      self.db.commit()
      
   def _update_ingredients(self, df):
      #sql = "DROP TABLE Ingredients"
      #self.cursor.execute(sql)
      sql = "CREATE TABLE IF NOT EXISTS Ingredients(id INT PRIMARY KEY AUTO_INCREMENT, ingredient VARCHAR(255) UNIQUE NOT NULL , allergen BOOLEAN DEFAULT False)"
      self.cursor.execute(sql)
      for i in range(len(df)):
         sql = "INSERT IGNORE INTO Ingredients (ingredient, allergen) VALUES (%s, %s)"
         val = (df.loc[i, 'ingredient'], int(df.loc[i, 'allergen']))
         self.cursor.execute(sql, val)
      self.db.commit()

   def _update_menu(self, df):
      #sql = "DROP TABLE Menu"
      #self.cursor.execute(sql)
      sql = "CREATE TABLE IF NOT EXISTS Menu(id INT PRIMARY KEY AUTO_INCREMENT, date DATETIME NOT NULL , dish_id INT, FOREIGN KEY (dish_id) REFERENCES Dishes(id))"
      self.cursor.execute(sql)
      for i in range(len(df)):
         sql = "SELECT id From Dishes WHERE dish = %s"
         val = (df.loc[i, 'name'],)
         self.cursor.execute(sql, val)
         dish_id = self.cursor.fetchone()[0]
         sql = "INSERT IGNORE INTO Menu (date, dish_id) VALUES (%s, %s)"
         val = (df.loc[i, 'date'], dish_id)
         self.cursor.execute(sql, val)
      self.db.commit()

   def _update_dishingredient(self, df):
      #sql = "DROP TABLE DishIngredient"
      #self.cursor.execute(sql)
      sql = "CREATE TABLE IF NOT EXISTS DishIngredient(id INT PRIMARY KEY AUTO_INCREMENT, dish_id INT, ingredient_id INT, FOREIGN KEY (dish_id) REFERENCES Dishes(id), FOREIGN KEY (ingredient_id) REFERENCES Ingredients(id))"
      self.cursor.execute(sql)
      for i in range(len(df)):
         sql, val = "SELECT id From Dishes WHERE dish = %s", (df.loc[i, 'name'],)
         self.cursor.execute(sql, val)
         dish_id = self.cursor.fetchone()[0]
         sql, val = "SELECT id From Ingredients WHERE ingredient = %s", (df.loc[i, 'ingredient'],)
         self.cursor.execute(sql, val)
         ingredient_id = self.cursor.fetchone()[0]
         sql = "INSERT IGNORE INTO DishIngredient (dish_id, ingredient_id) VALUES (%s, %s)"
         val = (dish_id, ingredient_id)
         self.cursor.execute(sql, val)
      self.db.commit()

def lambda_handler(event, context):
    datestr = (datetime.now() - timedelta(days=31) + timedelta(days=int(datetime.now().minute))).strftime('%Y-%m-%d')
    scraper = Scraper(datestr)
    database = Database(scraper._get_data())
    database._handle_data()
    print('data succesfully stored from\t' + str(datestr))
    datestr = (datetime.strptime(datestr, '%Y-%m-%d') - timedelta(days = 1)).strftime('%Y-%m-%d')
    return {
        'statusCode' : 200,
        'body' : 'success! collected and transferred data from day ' + datestr
    }
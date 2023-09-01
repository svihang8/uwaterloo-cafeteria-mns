import os
from dotenv import load_dotenv
import mysql.connector
import pymysql
import pandas as pd


class Database:
   load_dotenv()
   db = mysql.connect.connector(
      host = os.getenv('DATABASE_HOST'),
      user=os.getenv('DATABASE_USER'),
      password=os.getenv('DATABASE_PASSWORD'),
      database=os.getenv('DATABASE_DATABASE'),
      ssl_ca = "/Users/vihangshah/Documents/cafeteria/global-bundle.pem"
   )
   cursor = db.cursor(buffered=True)

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
         
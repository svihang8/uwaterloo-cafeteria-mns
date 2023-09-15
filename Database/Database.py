import os
from dotenv import load_dotenv
import mysql.connector
import pandas as pd
from datetime import datetime

class Database:
   load_dotenv()
   db = mysql.connector.connect(
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
   
   def _get_ingredients(self):
      sql = "SELECT ingredient FROM Ingredients"
      self.cursor.execute(sql)
      ingredients = []
      for ingredient in self.cursor.fetchall():
         print(ingredient)
         ingredients.append(ingredient[0])
      return ingredients


   def _create_user(self, name, phonenumber, notificationtime = '00:00:00', allergies = []):
      if not name or not phonenumber:
         return None
      sql = "CREATE TABLE IF NOT EXISTS Users(id INT PRIMARY KEY AUTO_INCREMENT, firstname VARCHAR(255) UNIQUE NOT NULL, phonenumber CHAR(10) UNIQUE NOT NULL, notificationtime TIME(0) DEFAULT '00:00:00')"
      self.cursor.execute(sql)
      sql = "INSERT IGNORE INTO Users (firstname, phonenumber, notificationtime) VALUES (%s, %s, %s)"
      val = (name, phonenumber, notificationtime)
      self.cursor.execute(sql, val)
      sql = "CREATE TABLE IF NOT EXISTS Allergies(id INT PRIMARY KEY AUTO_INCREMENT, user_id INT, ingredient_id INT)"
      self.cursor.execute(sql)
      sql = "SELECT id FROM Users WHERE firstname = %s"
      val = (name, )
      self.cursor.execute(sql, val)
      user_id = self.cursor.fetchone()[0]
      for i in range(len(allergies)):
         sql = "SELECT id from Ingredients WHERE ingredient = %s"
         val = (allergies[i], )
         self.cursor.execute(sql, val)
         ingredient_id = self.cursor.fetchone()[0]
         sql = "INSERT IGNORE INTO Allergies (user_id, ingredient_id) VALUES (%s, %s)"
         val = (user_id, ingredient_id)
         self.cursor.execute(sql, val)
      self.db.commit()

   def _get_notification_data(self, time = "00:00:00", date = datetime.now()):
       sql = "SELECT * FROM Users WHERE notificationtime = %s"
       val = (time, )
       self.cursor.execute(sql, val)
       users = self.cursor.fetchall()
       data = []
       for user in users:
          user_name = user[1]
          user_phonenumber = user[2]
          # sql query to get all allergies of user.
          sql = "SELECT ingredient_id FROM Allergies WHERE user_id = %s"
          val = (user[0], )
          self.cursor.execute(sql, val)
          allergens_ids = self.cursor.fetchall()
          # get dishes containing allergen. return list of dishes 
          dishes = []
          for allergen_id in allergens_ids:
             sql = "SELECT dish_id FROM DishIngredient WHERE ingredient_id = %s"
             val = (allergen_id[0], )
             self.cursor.execute(sql, val)
             dishes_ids = self.cursor.fetchall()
             for dish_id in dishes_ids:
                sql = "SELECT * FROM Menu WHERE dish_id = %s AND date = %s"
                date = datetime.today().replace(microsecond=0, second=0, minute=0, hour=0)
                val = (dish_id[0], date)
                self.cursor.execute(sql, val)
                current_dishes = self.cursor.fetchall()
                for current_dish in current_dishes:
                   sql = "SELECT dish FROM Dishes WHERE id = %s"
                   val = (current_dish[2], )
                   self.cursor.execute(sql, val)
                   dish_names = self.cursor.fetchall()
                   if dish_names:
                     for dish_name in dish_names:
                        dishes.append(dish_name[0])
          dishes = list(dict.fromkeys(dishes))
          data.append({
             'name' : user_name,
             'phonenumber' : user_phonenumber,
             'dishes' : ', '.join(dishes)
          })
       return data
                   
                



   
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
         
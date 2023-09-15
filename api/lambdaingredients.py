import json
import mysql.connector
import os

class Database:
    def __init__(self):
        self.db = mysql.connector.connect(
            host = os.environ['DATABASE_HOST'],
            user=os.environ['DATABASE_USER'],
            password=os.environ['DATABASE_PASSWORD'],
            database=os.environ['DATABASE_DATABASE'],
            )
        self.cursor = self.db.cursor(buffered=True)
    
    def _get_ingredients(self):
      sql = "SELECT ingredient FROM Ingredients"
      self.cursor.execute(sql)
      ingredients = []
      for ingredient in self.cursor.fetchall():
         ingredients.append(ingredient[0])
      return ingredients    


def lambda_handler(event, context):
    database = Database()
    ingredients = database._get_ingredients()
    return {
        'statusCode': 200,
        'body': ingredients,
    }

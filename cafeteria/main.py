from MenuScraper.Scraper import Scraper
from Database.Database import Database
from datetime import datetime, timedelta
import sys

def main():
   datestr = '2023-08-15'
   for i in range(1):
      scraper = Scraper(datestr)
      database = Database(scraper._get_data())
      database._handle_data()
      print('data succesfully stored from\t' + str(datestr))
      datestr = (datetime.strptime(datestr, '%Y-%m-%d') - timedelta(days = 1)).strftime('%Y-%m-%d')
   return 0

if __name__ == '__main__':
   sys.exit(main())
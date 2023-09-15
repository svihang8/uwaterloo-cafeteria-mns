import sys
sys.path.append('.')
from Database.Database import Database
from MenuScraper.Scraper import Scraper
from datetime import datetime, timedelta

def main():
   datestr = datetime.now().strftime('%Y-%m-%d')
   for i in range(10):
      scraper = Scraper(datestr)
      database = Database(scraper._get_data())
      database._handle_data()
      print('data succesfully stored from\t' + str(datestr))
      datestr = (datetime.strptime(datestr, '%Y-%m-%d') + timedelta(days = 1)).strftime('%Y-%m-%d')
   return 0

if __name__ == '__main__':
   sys.exit(main())
import schedule
import time 
import logging
import os
import json

from dotenv import load_dotenv

from scraper import get_data
from google_sheets import service_account


def main():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')

    load_dotenv()
    SHEET_ID = os.getenv("SHEET_ID")
    INFO = json.loads(os.getenv("INFO"))

    shop_id = ['59763733', '809769142', '63983008']
    # data = get_data(shop_id)
    
    sheet = service_account(SHEET_ID, INFO)
    # sheet.append_rows(data)
    print(sheet.get_all_values())


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')
    main()
    # schedule.every(1).days.do(get_data)
    # main()
    # while True:
    #     schedule.run_pending()
    #     time.sleep(3600)
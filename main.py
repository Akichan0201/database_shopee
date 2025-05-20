import requests
import datetime
import schedule
import time
import sqlite3
import pandas as pd
import logging
import numpy as np


def get_api(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36'
    } 
    response = requests.get(url, headers=headers)
    logging.info(f'Get {url} from api {response.status_code}')

    response.raise_for_status()
    return response.json()

def get_data():

    final_data = []
    # list of shop id
    shop_id = ['59763733', '809769142', '63983008']
    ratings = [i for i in range(1, 6)]
    for shop in shop_id:
        for rate in ratings:
            data_per_rating = get_rating(shop, rate)
            final_data.extend(data_per_rating)
            logging.info(f'Get data for rating {rate}')
    return final_data

def get_rating(shop_id, ratings):
    offset = 0
    limit = 6
    
    final_res = []
    status = True

    base_url = "https://shopee.co.id/api/v4/seller_operation/get_shop_ratings_new?"
    
    while status:
        api = get_api(f'{base_url}limit={limit}&offset={offset}&shopid={shop_id}&type={ratings}&userid=63984451')
        # validate
        try:
            data = collect_data(api)
            print(len(data))
            for i in data:
              product = [
                    i['orderid'],
                    i['itemid'],
                    i['userid'],
                    i['shopid'],
                    i['comment'],
                    i['rating_star'],
                    i['mtime'],
                    i['product_items'][0]['name']
              ]
            print(product)

            # UPDATE to DB
            conn = sqlite3.connect('shopee.db')
            df = pd.DataFrame(
                np.array(product).reshape(-1, 8), columns=['orderid', 'itemid', 'userid', 'shopid', 'comment', 'rating_star', 'mtime', 'product'])
            print(df)
            
            df.to_sql('shopee', conn, if_exists='append', index=False)
            print("=================SUCESSS UPDATE DATA===========================")

            time.sleep(2)
            offset += 6

            # DELETE FOR PROD
            if offset > 12:
                status = False
        except Exception as e:
            logging.info(f'No data: {e}')
            status = False
    return final_res

def unix_converter(mtime):
    try:
        dt = str(datetime.date.fromtimestamp(mtime))
        return dt
    except Exception as e:
        logging.error(e)
        raise ValueError("Cant convert to datetime", e)
    
def collect_data(response_api):
    date_now = str(datetime.datetime.now().date())
    collected_data = []
    for i in response_api['data']['items']: 
        
        # Replace unix time to more readable format
        mtime = i['mtime']
        dt = unix_converter(mtime)
        i['mtime'] = dt

        if dt == date_now:
            collected_data.append(i)
            # print(collected_data)
            logging.info(len(collected_data))
            
        else:
            logging.info(f'no data for today {date_now}')            
    return collected_data
    

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')
    get_data()
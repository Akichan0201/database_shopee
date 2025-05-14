import requests
import datetime
import schedule
import time
import sqlite3
import pandas as pd
import logging

from dataclasses import dataclass, asdict

logging.basicConfig(filename='main.log', level=logging.WARNING, format='%(asctime)s %(levelname)s:%(message)s')
date_now = str(datetime.datetime.now().date())

@dataclass
class Product():
    orderid: str
    itemid: str
    userid: str
    shopid: str
    comment: str
    rating_star: int
    mtime: str
    product: str


def get_api(url):
    print(url)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36'
    } 
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        logging.info(f'Get url from api {url}')

    response.raise_for_status()
    logging.info('Get data success')
    return response.json()

def get_data():

    final_data = []
    # list of shop id
    shop_id = ['59763733', '809769142', '63983008']
    ratings = [i for i in range(1, 6)] #[1,2,3,4,5]
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
            final_res.extend(data)

            time.sleep(2)
            offset += 6
            print('Offset:', offset)

            # DELETE FOR PROD
            if offset > 12:
                status = False
        except:
            logging.info('No data')
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

    collected_data = []
    for i in response_api['data']['items']: 
        
        # Replace unix time to more readable format
        mtime = i['mtime']
        dt = unix_converter(mtime)
        i['mtime'] = dt

        if dt == date_now:
            collected_data.append(i)
            logging.INFO(len(collected_data))
            
        else:
            print(dt, date_now)
            
    return collected_data
    

def main():
    
    data_json = get_data()
    data_shop = []
    
    for i in data_json:

        product = Product(
            i['orderid'],
            i['itemid'],
            i['userid'],
            i['shopid'],
            i['comment'],
            i['rating_star'],
            i['mtime'],
            i['product_items'][0]['name']
        )
        
        data_shop.append(product)
    return data_shop

def export_data():
    
    shopee = main() # list of object
    shopee = [asdict(item) for item in shopee]

    df = pd.DataFrame(shopee)
    conn = sqlite3.connect('shopee.db')
    df.to_sql('shopee', conn, if_exists='append', index=False)
   

if __name__ == '__main__':
    schedule.every(5).minutes.do(export_data)
    
    while True:
        schedule.run_all()
        print("running....")
        time.sleep(1)
    #print diganti dengan log
    #bikin scheduling biar running tiap hari
    #write seperti biasa log dibikin file baru(info)
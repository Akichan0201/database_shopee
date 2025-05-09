import requests
import datetime
import schedule
import time
import sqlite3
import pandas as pd
import logging

from dataclasses import dataclass, asdict

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
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36'
    } 
    response = requests.get(url, headers=headers)
    return response.json()

def get_data():
    #wardah
    offset = 0
    ratings = 5
    date_now = datetime.datetime.now().date()
    final_res = []
    status = True
    
    while status:
        #wardah
        # api = get_api(f'https://shopee.co.id/api/v4/seller_operation/get_shop_ratings_new?limit=6&offset={offset}&shopid=59763733&type={ratings}&userid=59765167')

        #glad2glow
        # api = get_api(f'https://shopee.co.id/api/v4/seller_operation/get_shop_ratings_new?limit=6&offset={offset}&shopid=809769142&type={ratings}&userid=809755351')

        #emina
        api = get_api(f'https://shopee.co.id/api/v4/seller_operation/get_shop_ratings_new?limit=6&offset={offset}&shopid=63983008&type={ratings}&userid=63984451')
        # validate
        try:
            for i in api['data']['items']: 
                #datetime     
                date = i['mtime']
                dt = datetime.date.fromtimestamp(date)
                # print(f"item date:{dt}, today:{date_now}")
                print(f"item date:{dt}, today:{date_now}")
                i['mtime'] = str(dt)

                if dt == date_now:
                    final_res.append(i)
                    print(len(final_res))
                else:
                    print(dt == date_now)
                    status = False
            
            time.sleep(2)
            offset += 6
            print('Offset:', offset)

            if offset > 12:
                status = False
        except:
            print('no data')
            status = False
    return final_res

def main():
    data_json = get_data()
    data_wardah = []
    data_glad2glow = []
    data_emina = []
    
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
        
        data_emina.append(product)
    return data_emina

if __name__ == '__main__':
    # print(get_data())
    schedule.every(5).minutes.do(main)
    emina = main() # list of object
    emina = [asdict(item) for item in emina]
    df = pd.DataFrame(emina)
    conn = sqlite3.connect('product.db')
    df.to_sql('schedule', conn, if_exists='append', index=False)

    while True:
        schedule.run_pending()
        time.sleep(1)
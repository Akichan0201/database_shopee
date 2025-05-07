import requests
import datetime
import time
import sqlite3
import pandas as pd

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
    print(response.status_code)
    # print(response.json())
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
        api = get_api(f'https://shopee.co.id/api/v4/seller_operation/get_shop_ratings_new?limit=6&offset={offset}&shopid=809769142&type={ratings}&userid=809755351')
        # validate
        try:
            for i in api['data']['items']: 
                #datetime     
                date = i['mtime']
                dt = datetime.date.fromtimestamp(date)
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
        
    #     data_wardah.append(product)
    # return data_wardah
        data_glad2glow.append(product)
    return data_glad2glow

if __name__ == '__main__':
    # print(get_data())
    glad2glow = main() # list of object
    glad2glow = [asdict(item) for item in glad2glow]
    df = pd.DataFrame(glad2glow)
    conn = sqlite3.connect('product_glad2glow.db')
    df.to_sql('product_glad2glow', conn, if_exists='append', index=False)
    print(glad2glow)
#https://baeftv87f5bqkgx2.canva-hosted-embed.com/codelet/AAEAEGJhZWZ0djg3ZjVicWtneDIAAAAAAZaVkH9gtCBPwc6QQA5Q2ykWk-AHnA73nHl4TMt4f0wMhvJ6iro/
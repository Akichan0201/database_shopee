import requests
import datetime
import time
import logging


def get_api(url:str)-> dict:
    """
    Get a json response from Shopee's API.

    :param url: the API endpoint to query
    :return: the JSON response
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
        'AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/135.0.0.0 Safari/537.36'
    }

    response = requests.get(url, headers=headers)

    response.raise_for_status()
    return response.json()


def unix_converter(mtime):
    try:
        date = str(datetime.date.fromtimestamp(mtime))
        return date
    except Exception as e:
        logging.error(e)
        return mtime
    

def time_converter(response_api:list[dict]):
    date_now = str(datetime.datetime.now().date())
    collected_data = []

    for i in response_api['data']['items']: 
        
        # Replace unix time to more readable format
        mtime = i['mtime']
        date = unix_converter(mtime)
        i['mtime'] = date

        # Collect data only if today
        if date == date_now:
            collected_data.append(i)            
        else:
            logging.warning(f'Current date: {date_now} Extracted date: {date}')            
    return collected_data


def extract_data(data:list[dict]):
    products = []
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
        products.append(product)
    return products
    

def get_rating(shop_id,ratings):
    offset = 0
    limit = 6
    final_res = []
    status = True

    base_url = "https://shopee.co.id/api/v4/seller_operation/get_shop_ratings_new?"

    while status:
        url = f'''{base_url}limit={limit}&offset={offset}&shopid={shop_id}&type={ratings}&userid=63984451'''
        logging.info(f"Processing {shop_id}, rating {ratings}, offset {offset}")

        data = get_api(url)

        # validate
        try:
            data = time_converter(data)

            if data == []: #break if no new data
                status = False
                
            data = extract_data(data)
            
            time.sleep(2)
            offset += 6

            final_res.extend(data)

            # DELETE FOR PRODUCTION
            if offset > 12:
                status = False

        except Exception as e:
            logging.error(f'No data: {e}')
            status = False
            
    return final_res


def get_data(shop_id: list):
    final_data = []
    ratings = [i for i in range(1, 6)]
    counter = len(shop_id)

    for i, shop in enumerate(shop_id):
        for rate in ratings:
            logging.info(f"Progress {((i+1)/counter)*100}%")
            data_per_rating = get_rating(shop, rate)
            final_data.extend(data_per_rating)
    return final_data


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')

    shop_id = ['59763733', '809769142', '63983008']
    data = get_data(shop_id)
    print(data)
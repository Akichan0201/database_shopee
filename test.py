import datetime
import logging
import time

print("Hello World")
logging.basicConfig(filename='log.log', level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')

def date():
    date_now = str(datetime.datetime.now())
    logging.info(f"Date: {date_now}")
    return date_now

if __name__ == '__main__':
    date()
    while True:
        print('running')
        time.sleep(5)



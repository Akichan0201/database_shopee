import schedule
import time

def job():
    print("I'm learning scheduling with python")
    with open ("sche.txt", "a") as f:
        f.write("I'm learning scheduling with python")

schedule.every(5).minutes.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
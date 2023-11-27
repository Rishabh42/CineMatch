import subprocess
import schedule
import time

def job(t):
    print(t)
    subprocess.run(["python3", "auto_deploy.py"])
    return

schedule.every().day.at("16:38").do(job,'It is 01:00, do periodic training and deployment')

while True:
    schedule.run_pending()
    # time.sleep(60) # wait one minute
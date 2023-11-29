# run in background: `nohup python3 scheduler.py &`
import subprocess
import schedule
import time

def job(t):
    print(t)
    subprocess.run(["python3", "auto_deploy.py"])
    return

schedule.every().day.at("18:12").do(job,'Periodic training and deployment scheduled successfully')

while True:
    # Run pending tasks
    schedule.run_pending()
    # Sleep for 1 minute
    time.sleep(60)
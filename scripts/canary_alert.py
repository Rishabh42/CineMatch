import requests
import json
import sys

# This script will be called from /home/team-4/team-4/app
# python3 ../scripts/canary_alert.py

sys.path.append('auto_deployment/')
from emailer import send_email

message = "The Canary release could not be deployed. Switching from canary to stable deployment. The average response time was more than 500ms."

def slack_post():
    url = 'https://hooks.slack.com/services/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'
    payload = {"text": message}
    json_payload = json.dumps(payload)

    # Set the headers to indicate that the payload is in JSON format
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, data=json_payload, headers=headers)

    # Check the response status
    if response.status_code == 200:
        print('POST request successful')
    else:
        print(f'POST request failed with status code {response.status_code}')

def email_alert():
    send_email("ALERT: Canary release was aborted.", message)

if __name__ == "__main__":
    email_alert()
    slack_post()

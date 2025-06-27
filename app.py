from db import db
from bson.json_util import dumps  # handles ObjectId and datetime
from bson.objectid import ObjectId
import json
import requests

# Define the collection you're working with
collection = db["mycollection"]

PAGERDUTY_ROUTING_KEY = "92f7e6e28674460ec0d4e29150623100"
API_TO_CHECK = "https://www.google.com"  

print(f"Fetching api1 data from the database...")
raw_data = collection.find_one({"api_name": "server_health"})
json_data = dumps(raw_data)
json_data = json.loads(json_data) 
api1_data = json_data["api_status"]

print(f"Fetching api1 current status")

try:
    response = requests.get(API_TO_CHECK, timeout=5)
    if response.status_code == 200:
        print(f"API is already working, no need to take any action")
        api1_current_status = 1
    else:
        print(f"⚠️ API responded with status: {response.status_code}")
        # handle unexpected status codes
        api1_current_status = 0
except requests.exceptions.Timeout:
    print("❌ Request timed out.")
    api1_current_status = 0
except requests.exceptions.ConnectionError:
    print("❌ Could not connect to the API. Host unreachable or DNS issue.")
    api1_current_status = 0
except requests.exceptions.HTTPError as e:
    print(f"❌ HTTP error occurred: {e}")
    api1_current_status = 0
except requests.exceptions.RequestException as e:
    print("❌ Something went wrong while checking the API.")
    api1_current_status = 0

print(f"checking api1 data and current status and applying logic...")
if api1_data == 0 and api1_current_status == 0:
    print(f"API is already down, suppport team already notified, no need to take any action")
    exit();
elif api1_data == 1 and api1_current_status == 1:
    print(f"API is already working, no need to take any action")
    exit();
elif api1_data == 0 and api1_current_status == 1:
    print(f"API is started working, updating the database to online...")
    update_result = collection.update_one(
        {"api_name": "server_health"},  # Filter to find the document
        {"$set": {"api_status":1}}  # Update operation
    )
    exit();
elif api1_data == 1 and api1_current_status == 0:
    print(f"API is stopped working, updating the database, notifiying support team...")
else:
    print(f"⚠️ Unknown API status, please check the code")



print(f"Notifying support team...")
def send_pagerduty_alert():
    payload = {
        "routing_key": PAGERDUTY_ROUTING_KEY,
        "event_action": "trigger",
        "payload": {
            "summary": f"API Health Check Failed: {API_TO_CHECK}",
            "severity": "critical",
            "source": "Alert source"
        },
    }

    url = "https://events.pagerduty.com/v2/enqueue"
    headers = {
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=5)
        response.raise_for_status()
        print("PagerDuty Response:", response.text)
        print(f"Updating database to set api_status to 0")
        update_result = collection.update_one(
            {"api_name": "server_health"},  # Filter to find the document
            {"$set": {"api_status":0}}  # Update operation
        )
    except requests.exceptions.HTTPError as e:
        print(f"PagerDuty HTTP Error: {e.response.status_code} - {e.response.reason}")
        print(e.response.text)
    except requests.exceptions.RequestException as e:
        print(f"PagerDuty Request Error: {str(e)}")

send_pagerduty_alert()


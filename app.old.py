from db import db
from bson.json_util import dumps  # handles ObjectId and datetime
from bson.objectid import ObjectId
import json

# Define the collection you're working with
collection = db["mycollection"]

# Sample document to insert
server_data = {
    "api_name":"server_health",
    "api_status":"1"
}

# -----------------------------------------------------------
# Insert the sample document
# insert_result = collection.insert_one(server_data)
# print(f"Inserted document ID: {insert_result.inserted_id}")

# ------------------------------------------------------------

# update the document to online
# update_result = collection.update_one(
#     {"api_name": "server_health"},  # Filter to find the document
#     {"$set": {"api_status": "1"}}  # Update operation
# )
# ------------------------------------------------------------

# update the document to offline
# update_result = collection.update_one(
#     {"api_name": "server_health"},  # Filter to find the document
#     {"$set": {"api_status":1}}  # Update operation
# )

# ----------------------------------------------------------

# Fetch a single document
raw_data = collection.find_one({"api_name": "server_health"})

# Convert to JSON string then json object (python dict)
json_data = dumps(raw_data)
json_data = json.loads(json_data) 




# Check api_status and apply conditions
if json_data["api_status"] == 1:
    print(f"✅ API '{json_data['api_name']}' is UP.")
elif json_data["api_status"] == 0:
    exit()
else:
    print("⚠️ Unknown API status.")

# ------------------------------------------------------
# Retrieve and print all documents from the collection
print("\nYour json data:")
print(json_data)
print("\n\n")

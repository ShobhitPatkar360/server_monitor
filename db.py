from pymongo import MongoClient

# MongoDB connection URI (update with your details if needed)
MONGO_URI = "mongodb+srv://shubhpatkar2000:Password1@cluster0.oyg1o.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"  # Replace with your MongoDB URI

# Connect to MongoDB
client = MongoClient(MONGO_URI)

# Connect to the 'testdb' database and 'users' collection
db = client["mydb"]
collection = db["mycollection"]
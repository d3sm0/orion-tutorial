from pymongo import MongoClient

# Step 1: Connect to MongoDB - Note: Change connection string as needed
host = "mongodb://95.217.133.223:27017"
client = MongoClient(host)
print(client.admin.command("ping"))

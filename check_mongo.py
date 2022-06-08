from pymongo import MongoClient

# Step 1: Connect to MongoDB - Note: Change connection string as needed
host = 'mongodb://95.217.133.223'
client = MongoClient(host)

print(client["orion_test"])
print(client.admin.command("ping"))

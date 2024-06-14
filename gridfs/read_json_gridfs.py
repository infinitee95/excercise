from pymongo import MongoClient
from gridfs import GridFS
import json

client = MongoClient('mongodb://localhost:27017/')  # Adjust the connection string as necessary
db = client['test_db']  # Replace with your database name
fs = GridFS(db)

filename = "api_json_exercise.json"

# Retrieve the file from GridFS
file = fs.find_one({'filename': filename})
retrieved_data = file.read().decode('utf-8')

# Convert the JSON string back to a dictionary
retrieved_json_data = json.loads(retrieved_data)

# Print the retrieved JSON data
print(retrieved_json_data)

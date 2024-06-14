from pymongo import MongoClient
from gridfs import GridFS
import json

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['test_db']
fs = GridFS(db)

# Step 2: Open and read the JSON file
json_file_path = '/home/user/Desktop/code/api_json_excercise.json'  # Replace with the path to your JSON file
with open(json_file_path, 'r') as file:
    json_data = json.load(file)

# Convert JSON data to string, as GridFS stores files as binary data
json_str = json.dumps(json_data)

# Store the JSON data in GridFS
file_id = fs.put(json_str.encode('utf-8'), filename='api_json_exercise.json', encoding='utf-8')

# Print the file ID to confirm the storage
print(f'JSON file stored in GridFS with file ID: {file_id}')

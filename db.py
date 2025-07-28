from pymongo import MongoClient

# Connect to MongoDB (localhost)
client = MongoClient("mongodb://localhost:27017/")

# Use or create database
db = client["legal_quiz_game"]

# Collections
users_collection = db["users"]
progress_collection = db["progress"]

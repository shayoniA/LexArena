from pymongo import MongoClient
import os
from dotenv import load_dotenv
load_dotenv()
mongo_uri = os.getenv("MONGO_URI")

# Connect to MongoDB
client = MongoClient(mongo_uri)

# Use or create database
db = client["legal_quiz_game"]

# Collections
users_collection = db["users"]
progress_collection = db["progress"]
questions_collection = db["questions"]
descriptions_collection = db["descriptions"]
classifier_collection = db["next_question_classifier"]
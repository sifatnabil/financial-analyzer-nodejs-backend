from pymongo import MongoClient
from dotenv import dotenv_values
from bson import ObjectId

def get_collection(db_name="TransactionDB", collection_name="transactions"):
   # Fetch the configuration settings
    config = dotenv_values(".env")
 
    # Provide the mongodb atlas url to connect python to mongodb using pymongo
    CONNECTION_STRING = config["MONGO_CONNECTION_STRING"]
    
    # Create a connection using MongoClient
    client = MongoClient(CONNECTION_STRING)
    
    # Get the database collection instance
    return client[db_name][collection_name]


def get_prompts(ids):
   # Get the MongoDB collection
   collection = get_collection(collection_name="prompts")

   # Retrieve the paragraphs from MongoDB
   paragraphs = []
   for paragraph_id in ids:
      paragraph = collection.find_one({"_id": ObjectId(paragraph_id)})
      if paragraph:
         paragraphs.append(paragraph["text"])

   # Return the paragraphs in a JSON response
   return paragraphs
from pymongo import MongoClient
from dotenv import dotenv_values

def get_collection(db_name="TransactionDB", collection_name="transactions"):
   # Fetch the configuration settings
    config = dotenv_values(".env")
 
    # Provide the mongodb atlas url to connect python to mongodb using pymongo
    CONNECTION_STRING = config["MONGO_CONNECTION_STRING"]
    
    # Create a connection using MongoClient
    client = MongoClient(CONNECTION_STRING)
    
    # Get the database collection instance
    return client[db_name][collection_name]
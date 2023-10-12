from pymongo import MongoClient
from dotenv import dotenv_values

def get_database(db_name="TransactionDB", collection_name="transactions"):
   # Fetch the configuration settings
    config = dotenv_values(".env")
 
    # Provide the mongodb atlas url to connect python to mongodb using pymongo
    CONNECTION_STRING = config["MONGO_CONNECTION_STRING"]
    
    # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
    client = MongoClient(CONNECTION_STRING)
    
    # Create the database for our example (we will use the same database throughout the tutorial
    return client[db_name][collection_name]
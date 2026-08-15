from pymongo import MongoClient
from dotenv import load_dotenv
import os
from bson.objectid import ObjectId

# Load .env file
load_dotenv()
db_connection=os.getenv("CONNECT_DB")

def update_record(uploadedfilename: str, id:str):
    """Upload file info to mongo db"""
    
    cluster = MongoClient(db_connection)

    # database
    db = cluster["songs"]
    # collections
    collection = db["audiofiles"]
    new_values = {"$set": {"outputFile": uploadedfilename,
            "status": "processed",}}

    db_result=collection.update_one({"_id": ObjectId(id)}, new_values)

    return db_result




def getInfo(id: str):
    """Upload file info to mongo db"""
    
    cluster = MongoClient(db_connection)

    # database
    db = cluster["songs"]
    # collections
    collection = db["audiofiles"]

    objInstance = ObjectId(id)
    db_result=collection.find_one({"_id": objInstance})
    

    return db_result
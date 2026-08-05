from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Load .env file
load_dotenv()
db_connection=os.getenv("CONNECT_DB")

def upload(uploadedfilename: str, inputfileName:str):
    """Upload file info to mongo db"""
    
    cluster = MongoClient(db_connection)

    # database
    db = cluster["songs"]
    # collections
    collection = db["audiofile"]

    db_result=collection.insert_one(
    {"input_file_name": inputfileName,
    "uploaded_file_name": uploadedfilename,
    })

    return db_result
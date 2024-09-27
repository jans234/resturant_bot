import os
from dotenv import load_dotenv
from pymongo import MongoClient, ASCENDING, DESCENDING
load_dotenv()
def insert_chat(**kwargs):
    con=os.getenv("MONGODB")
    with MongoClient(con) as client:
        client["FastFoodDeals"]["chats"].insert_one(kwargs)

def fetch_chats(userid:str):
    con=os.getenv("MONGODB")
    with MongoClient(con) as client:
        cursor= client["FastFoodDeals"]["chats"].find({"userid":userid}).sort("created_at",DESCENDING).limit(6)
        chats= list(cursor)
        return(chats)
    
def fetch_images(image_ids:list):
    images = []
    con=os.getenv("MONGODB")
    with MongoClient(con) as client: 
        for id_ in image_ids:
            cursor= client["FastFoodDeals"]["deals"].find({"id": id_})
            cursor = list(cursor)
            cursor[0].pop('_id')
            images.extend(cursor)
    return images
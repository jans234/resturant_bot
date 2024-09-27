from chromadb_service import retriver
from prompt import PROMPT
from openai_service import AskAI
from mongodb_service import *
import datetime
from logger import *
import re
import json

def restaurant_chatbot(userid:str,question:str):
    try:
        log.info("Adding Chats into MongoDB -- User")
        insert_chat(
            userid=userid,
            role="user",
            msg=question,
            created_at=datetime.datetime.now()
        )
        log.info("Retriving Data From Database")
        docs = retriver(question)
        image_ids = extract_ids(docs)
        images = fetch_images(image_ids)
        log.info(f"Found Images: {images}")
        DOC_PROMPT = 'This is from where you can possibly get information about the user question'
        for doc in docs:
            DOC_PROMPT += "\n" + doc
        messages = [
            {
                "role": "system",
                "content": PROMPT
            },
            {
                "role": "system",
                "content": f"This is the deal info: {DOC_PROMPT},\nThese are the images associated with the deals {json.dumps(images)}"
            },
            
        ]

        try:
            log.info("Fetching Chats from MongoDB")
            chats = fetch_chats(userid)
            for chat in chats:
                    messages.append(
                    {
                        "role":chat['role'],
                        "content":chat["msg"]
                    }
                    )
        except Exception as e:
            pass
    
        messages.append({"role":"user","content":question})

        response = AskAI(messages)
        log.info("Adding Chats into MongoDB -- AI")
        insert_chat(
            userid=userid,
            role="assistant",
            msg=response,
            created_at=datetime.datetime.now()
        )
        return response
    except Exception as e:
        log.error(e,exc_info=True)

def extract_ids(data):
    # Use regex to find IDs that start with * followed by numbers and end with *
    ids = []
    log.info(f"Vector Database: {data}")
    for deal in data:
        log.info(f"Deals Found: {deal}")

        single_id = re.findall(r'ID:\s*(\d{23})', deal)
        if single_id:
            ids.append(single_id)
    ids = [id_[0] for id_ in ids]
    log.info(f"Extracted Ids: {ids}")
    return ids


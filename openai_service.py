from openai import OpenAI
from dotenv import load_dotenv
from logger import *

load_dotenv()


def AskAI(messages:list):
    log.info("Fetching OpenAI response")
    client = OpenAI()
    response = client.chat.completions.create(
    temperature=0,
    model="gpt-4o-mini",
    messages=messages
    )
    return response.choices[0].message.content
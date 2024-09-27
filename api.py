from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from resturant_chatbot import *
from logger import *

# Initialize FastAPI app
app = FastAPI()

# Define a Pydantic model for the request body
class QuestionRequest(BaseModel):
    question: str

# FastAPI endpoint for the chatbot
@app.post("/ask_deals")
def ask_deals(question_request: QuestionRequest):
    question = question_request.question
    log.info(f"Request:{question_request}")
    try:
        # Use the resturant_chatbot function to get the response
        answer = restaurant_chatbot("123",question)
        log.info(answer)
        
        return {"answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


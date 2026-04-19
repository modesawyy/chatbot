from openai import OpenAI
from fastapi import FastAPI
from pydantic import BaseModel
import os
from dotenv import load_dotenv
load_dotenv()


app = FastAPI()

client = OpenAI(
    api_key=os.getenv("APIKEY"))

class ChatRequest(BaseModel):
    msg: str


systemprompt = """ You are a professional pet care assistant.

Rules:
- ONLY answer questions related to animals (pets, health, care, feeding, behavior).

- If the question is NOT related to animals:
  - If the user writes in Arabic, respond in Arabic:
    "🐶🐱 أنا متخصص في رعاية الحيوانات، فمقدرش أساعد في السؤال ده 😊 ، لو عندك أي سؤال عن الحيوانات  أنا معاك "
  - If the user writes in English, respond in English:
    "Sorry, I can only help with animal-related questions 😊😻🐶 ."

- If the question IS about animals:
  - Respond in the SAME language as the user (Arabic or English).

- Keep answers short, clear, and helpful.
"""

conversation = []


@app.post('/chat')
async def chat(request: ChatRequest):

    if not conversation:
        conversation.append({
            'role': 'developer',
            'content': systemprompt
        })

    conversation.append({
        'role': 'user',
        'content': request.msg
    })

    try:
        response = client.responses.create(
            model='gpt-5.4-mini',
            input=conversation
        )

        conversation.append({
            "role": "assistant",
            "content": response.output_text
        })

        return {"Response": response.output_text}

    except Exception as e:
        return {"error": str(e)}
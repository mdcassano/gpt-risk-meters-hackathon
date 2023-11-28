import os
import json
from openai import AzureOpenAI
from fastapi import FastAPI
from testchat import get_chat_response
from fastapi.middleware.cors import CORSMiddleware

    

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/prompt")
def read_item(q: str):
    return json.loads(get_chat_response(q))
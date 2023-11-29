import os
import json
from openai import AzureOpenAI
from fastapi import FastAPI
from testchat import Chat
from fastapi.middleware.cors import CORSMiddleware

    

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['https://testkenna.kdev.docker'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/prompt")
def read_item(q: str, direction: str=""):
    chat = Chat(query=q, prefix=direction)
    return json.loads(chat.response())
import os
import json
from openai import AzureOpenAI
from fastapi import FastAPI
from testchat import load_prompts_from_file_system
from fastapi.middleware.cors import CORSMiddleware
# from pydantic import BaseModel

# class Prompt(BaseModel):
#     q: str
    

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
    client = AzureOpenAI(
        azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT"), 
        api_key=os.getenv("AZURE_OPENAI_KEY"),  
        api_version="2023-05-15" # TODO: is this a good date?
    )

    system_prompt, user_prompt = load_prompts_from_file_system()
    response = client.chat.completions.create(
        model="hack-gpt-4",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": q}
        ]
    )

    return json.loads(response.choices[0].message.content)
import os
import sys
from openai import AzureOpenAI

client = AzureOpenAI(
  azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT"), 
  api_key=os.getenv("AZURE_OPENAI_KEY"),  
  api_version="2023-05-15"
)

prompt_prefix = ""
if len(sys.argv) > 1:
    prompt_prefix = sys.argv[1] + "-"

with open("%ssystem.prompt" % (prompt_prefix)) as f:
    system_prompt = f.read()

with open("%suser.prompt" % (prompt_prefix)) as f:
    user_prompt = f.read()

response = client.chat.completions.create(
    model="hack-gpt-4",
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]
)

print(response.choices[0].message.content)

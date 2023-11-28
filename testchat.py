import os
import sys
from openai import AzureOpenAI

def load_system_prompt(prompt_prefix=""):
    with open("base-locator-description.prompt") as f:
        base_prompt = f.read()
    
    with open("%ssystem.prompt" % (prompt_prefix)) as f:
        system_prompt = f.read()
    
    system_prompt = base_prompt + "\n\n" + system_prompt
    
    return system_prompt

def load_user_prompt(prompt_prefix=""):
    with open("%suser.prompt" % (prompt_prefix)) as f:
        user_prompt = f.read()
    return user_prompt

client = AzureOpenAI(
  azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT"), 
  api_key=os.getenv("AZURE_OPENAI_KEY"),  
  api_version="2023-05-15" # TODO: is this a good date?
)

def get_chat_response(user_prompt=None, prefix=""):
    system_prompt = load_system_prompt(prefix)

    response = client.chat.completions.create(
        model="hack-gpt-4",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    )
    return response.choices[0].message.content


if __name__ == "__main__":
    prompt_prefix = ""
    if len(sys.argv) > 1:
        prompt_prefix = sys.argv[1] + "-" 

    print(get_chat_response(load_user_prompt(prompt_prefix)))
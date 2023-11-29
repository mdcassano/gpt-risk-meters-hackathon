import json
import os
import sys
from openai import AzureOpenAI
from openai._exceptions import OpenAIError
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env

class Chat:
    def __init__(self, query=None, prefix=None):
        self.prefix = prefix
        self.query = query or self.load_user_prompt()

    def load_system_prompt(self):
        with open("base-locator-description.prompt") as f:
            base_prompt = f.read()
        
        with open("%ssystem.prompt" % self.prompt_prefix) as f:
            system_prompt = f.read()
        
        return base_prompt + "\n\n" + system_prompt

    def load_user_prompt(self):
        with open("%suser.prompt" % self.prompt_prefix) as f:
            user_prompt = f.read()
        return user_prompt

    @property
    def prompt_prefix(self):
        if self.prefix:
            return self.prefix + "-"
        elif self.prefix == None and len(sys.argv) > 1:
            return sys.argv[1] + "-"
        else:
            return ""

    @property
    def client(self):
        return AzureOpenAI(
            azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT"), 
            api_key=os.getenv("AZURE_OPENAI_KEY"),  
            api_version="2023-05-15" # TODO: is this a good date?
        )

    def response(self):
        system_prompt = self.load_system_prompt()

        response = self.client.chat.completions.create(
            model="hack-gpt-4",
            temperature=0,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": self.query}
            ]
        )
        return response.choices[0].message.content
    
    def syntax_output(self):
        response = json.loads(self.response())
        try:
            return response["syntax"]
        except KeyError:
            raise OpenAIError(response["error"])

    def description_output(self):
        response = json.loads(self.response())
        try:
            return response["description"]
        except KeyError:
            raise OpenAIError(response["error"])


if __name__ == "__main__":
    chat = Chat()
    print(chat.response())
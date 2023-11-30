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
        if query is not None:
            self.query = query
        else:
            self.query = self.load_query()

    def load_system_messages(self):
        with open("prompts/main.json") as f:
            return json.load(f)["messages"]

    def load_query(self):
        with open("%squery.txt" % self.prompt_prefix) as f:
            user_prompt = f.read()
        return user_prompt

    def load_user_message(self):
        with open("prompts/%suser.txt" % self.prompt_prefix) as f:
            user_prompt = f.read()
        return {"role": "user", "content": user_prompt.format(self.query)}

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
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            api_key=os.getenv("AZURE_OPENAI_KEY"),
            api_version="2023-05-15",  # TODO: is this a good date?
        )

    def response(self):
        messages = self.load_system_messages()
        messages.append(self.load_user_message())

        response = self.client.chat.completions.create(
            model="hack-gpt-35",
            temperature=0,
            messages=messages,
        )
        content = response.choices[0].message.content
        print(content)
        return content

    def query_output(self):
        response = json.loads(self.response())
        try:
            return response["query"]
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

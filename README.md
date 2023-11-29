Using python 3.11.6 and pipenv:

```
brew install pipenv
pipenv sync
pipenv shell
```

Set your environment variables in .env

```
cat "AZURE_OPENAI_KEY=<MIKE HAS THE KEY>" > .env
cat "AZURE_OPENAI_ENDPOINT=https://cloudsec-hackathon-apim.azure-api.net/" >> .env
```

Using the text in system.prompt and user.prompt, run the chat completion:

```
python ./testchat.py
```

By default, the script will use system.prompt and user.prompt. If you want to use a different set of files, for instance reverse-system.prompt and reverse-user.prompt, pass in the file prefix as the first parameter:

```
python ./testchat.py reverse
```

Run fastapi

```
uvicorn main:app --reload
```

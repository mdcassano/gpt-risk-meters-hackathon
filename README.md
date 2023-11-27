Using python 3.9.6, install openai

```
pip install openai
```

Set your environment variables

```
export AZURE_OPENAI_KEY=<MIKE HAS THE KEY>
export AZURE_OPENAI_ENDPOINT=https://cloudsec-hackathon-apim.azure-api.net/
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

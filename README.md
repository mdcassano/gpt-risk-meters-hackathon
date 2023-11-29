# ChatGPT Risk Meters

## Installing

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

## CLI

Using the text in system.prompt and user.prompt, run the chat completion:

```
python ./testchat.py
```

By default, the script will use system.prompt and user.prompt. If you want to use a different set of files, for instance reverse-system.prompt and reverse-user.prompt, pass in the file prefix as the first parameter:

```
python ./testchat.py reverse
```

## Integrating with conduit

Use the [gpt-risk-meters-hackathon](https://github.com/KennaSecurity/conduit/tree/gpt-risk-meters-hackathon) branch of conduit and start fastapi:

```
uvicorn main:app --reload
```

## Testing

The test suite consists of YAML files in `tests/` that contain a risk meter query and the description that generates it.

Each example is also tested in reverse: GPT generates a description, then that description is tested to see if it returns the original query.

To run all examples in parallel:

```
pytest -n auto
```

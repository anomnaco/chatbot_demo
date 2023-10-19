## API Readme

# Setup

This readme is for a FastAPI api that uses pydantic to parse incoming data. That data is used to retreive documents from an Astra vector store and then both the original query and the user input are used to construct a prompt. That prompt is sent to OpenAI and the api returns the response to the user.

Then clone this repo and install the Python requirements (This demo assumes you already have python3 installed):
```
git clone https://github.com/Anant/astra-chatbot-react-python.git
pip3 install -r requirements.txt
```

Input all of you authentication credentials into local_creds.py. This file requries your Astra client id and secret, the name of the Astra secure connect bundle for your database. It also needs the keyspace name and table name for your vector store. Lastly it requries your OpenAI api key. Make sure to also load in your secure connect bundle zip file into astra-chatbot-react-python/api. 

# Start Process

To run the api enter the command:
```
uvicorn api.index:app --reload
```

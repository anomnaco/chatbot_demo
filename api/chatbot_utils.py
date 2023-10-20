import json
import requests
from api.local_creds import *

request_url = f"https://{ASTRA_DB_ID}-{ASTRA_DB_REGION}.apps.astra.datastax.com/api/json/v1/{KEYSPACE_NAME}/{COLLECTION_NAME}"
request_headers = { 'x-cassandra-token': app_token,  'Content-Type': 'application/json'}

#langchain openai interface
completion_url = "https://api.openai.com/v1/chat/completions"
completion_headers = {'Content-Type':'application/json', 'Authorization':'Bearer '+OPENAI_API_KEY}

def get_completion_body(text):
    return {"model": "gpt-3.5-turbo",
            "messages":[{"role": "user", "content": text}]
   }

def predict(text):
    response = requests.request("POST", completion_url, headers=completion_headers, data=json.dumps(get_completion_body(text)))
    return response.json()['choices'][0]['message']['content']


embedding_url = "https://api.openai.com/v1/embeddings"
embedding_headers = {'Content-Type':'application/json', 'Authorization':'Bearer '+OPENAI_API_KEY}

def get_embedding_body(text):  
    return {"input": text, "model": "text-embedding-ada-002"}

def embed_query(text):
    response = requests.request("POST", embedding_url, headers=embedding_headers, data=json.dumps(get_embedding_body(text)))
    return response.json()['data'][0]['embedding']

def get_similar_docs(query, number):
    embedding = list(embed_query(query))
    payload = json.dumps({"find": {"sort": {"$vector": embedding},"options": {"limit": number}}})
    relevant_docs = requests.request("POST", request_url, headers=request_headers, data=payload).json()['data']['documents']
    #print(relevant_docs)
    docs_contents = [row['answer'] for row in relevant_docs] 
    docs_urls = [row['document_id'] for row in relevant_docs]
    return docs_contents, docs_urls
    
#promt that is sent to openai using the response from the vector database and the users original query
prompt_boilerplate = "Answer the question posed in the user query section using the provided context"
user_query_boilerplate = "USER QUERY: "
document_context_boilerplate = "CONTEXT: "
final_answer_boilerplate = "Final Answer: "

def build_full_prompt(query):
    relevant_docs, urls = get_similar_docs(query, 3)
    docs_single_string = "\n".join(relevant_docs)
    all_urls = set([url for url in urls])

    nl = "\n"
    filled_prompt_template = prompt_boilerplate + nl + user_query_boilerplate+ query + nl + document_context_boilerplate + docs_single_string + nl + final_answer_boilerplate
    print(filled_prompt_template)
    return filled_prompt_template, list(all_urls)


def send_to_openai(full_prompt):
    return predict(full_prompt)


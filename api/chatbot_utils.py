from langchain.prompts import PromptTemplate
import json
import requests
from langchain.llms import OpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores.cassandra import Cassandra
from local_creds import *

request_url = f"https://{ASTRA_DB_ID}-{ASTRA_DB_REGION}.apps.astra.datastax.com/api/json/v1/{KEYSPACE_NAME}/{COLLECTION_NAME}"
request_headers = { 'x-cassandra-token': app_token,  'Content-Type': 'application/json'}

#langchain openai interface
llm = OpenAI(openai_api_key=OPENAI_API_KEY)
embedding_model = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY) 

from operator import itemgetter
def get_similar_docs(query, number):
    embedding = list(embedding_model.embed_query(query))
    payload = json.dumps({"find": {"sort": {"$vector": embedding},"options": {"limit": number}}})
    relevant_docs = requests.request("POST", request_url, headers=request_headers, data=payload).json()['data']['documents']
    #print(relevant_docs)
    docs_contents = [row['answer'] for row in relevant_docs] 
    docs_urls = [row['document_id'] for row in relevant_docs]
    return docs_contents, docs_urls
    
#promt that is sent to openai using the response from the vector database and the users original query
prompt_boilerplate = "Answer the question posed in the user query section using the provided context"
user_query_boilerplate = "USER QUERY: {userQuery}"
document_context_boilerplate = "CONTEXT: {documentContext}"
final_answer_boilerplate = "Final Answer: "

def build_full_prompt(query):
    relevant_docs, urls = get_similar_docs(query, 3)
    docs_single_string = "\n".join([doc.page_content for doc in relevant_docs])
    all_urls = set([url for url in urls])

    nl = "\n"
    combined_prompt_template = PromptTemplate.from_template(prompt_boilerplate + nl + user_query_boilerplate + nl + document_context_boilerplate + nl + final_answer_boilerplate)
    print(combined_prompt_template)
    filled_prompt_template = combined_prompt_template.format(userQuery=query, documentContext=docs_single_string)
    print(filled_prompt_template)
    return filled_prompt_template, list(all_urls)


def send_to_openai(full_prompt):
    return llm.predict(full_prompt)


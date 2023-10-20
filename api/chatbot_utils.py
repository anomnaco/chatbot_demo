from langchain.prompts import PromptTemplate

from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from api.local_creds import *

from langchain.llms import OpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores.cassandra import Cassandra

#Astra db connection
cloud_config= { 'secure_connect_bundle': secure_bundle_path , 'use_default_tempdir': True}
auth_provider = PlainTextAuthProvider(client_id, client_secret)
cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
session = cluster.connect()


#langchain openai interface
llm = OpenAI(openai_api_key=OPENAI_API_KEY)
embedding_model = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY) 

#langchain Cassandra vector store interface
astraVectorStore = Cassandra( embedding=embedding_model, session=session, keyspace=db_keyspace, table_name=db_table)
from operator import itemgetter
def get_similar_docs(query, number):
    embedding = list(embedding_model.embed_query(query))
    relevant_docs = astraVectorStore.similarity_search_with_score_id_by_vector(embedding, number)
    docs_contents = map(itemgetter(0), relevant_docs)
    docs_urls = map(itemgetter(2), relevant_docs)
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

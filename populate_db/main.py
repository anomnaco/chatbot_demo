import json
import os

import split_q_and_a
from constants import INPUT_JSON, SCB_PATH, TOKEN_ID, TOKEN_SECRET

from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from sentence_transformers import SentenceTransformer
from langchain.embeddings import OpenAIEmbeddings

import time
import sys
sys.path.append('../api')
from local_creds import *
#To do: add logger
embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)

def get_input_data():
    scraped_results_file = INPUT_JSON
    with open(scraped_results_file) as f:
        scraped_data = json.load(f)

        faq_scraped_data = []
        for d in scraped_data:
            if "faq" in d["url"].lower():
                faq_scraped_data.append(d)
    return faq_scraped_data


def connect_to_astra():
    # connect to astra vector search db
    cloud_config = {'secure_connect_bundle': SCB_PATH}
    auth_provider = PlainTextAuthProvider(TOKEN_ID, TOKEN_SECRET)
    cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
    session = cluster.connect()
    return session


def embed(text_to_embed):
    embedding = list(embeddings.embed_query(text_to_embed))
    return embedding


def main():
    session = connect_to_astra()
    print(session)

    input_data_faq = get_input_data()

    # process faq data
    for webpage in input_data_faq:
        q_and_a_data = split_q_and_a.split(webpage)

        for i in range (0,len(q_and_a_data["questions"])):
            document_id = webpage["url"]
            question_id = i + 1
            question = q_and_a_data["questions"][i]
            answer = q_and_a_data["answers"][i]
            text_to_embed = f"{question} {answer}"
            embedding = embed(text_to_embed)
            time.sleep(5)

            session.execute("""INSERT INTO vector_search_ai.qadoc_openai
                (document_id, index_id, document, question, vector) VALUES (%s, %s, %s, %s, %s)""",
                (document_id, question_id, answer, question, embedding))


if __name__ == "__main__":
    main()

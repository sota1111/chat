import json
import os
import boto3
import openai

from llama_index import SimpleDirectoryReader
from llama_index import Document
from llama_index import GPTListIndex

from dotenv import load_dotenv
load_dotenv()

API_KEY_ENV_NAME = 'API_Key'
OPENAI_API_KEY = os.environ[API_KEY_ENV_NAME]
openai.api_key = OPENAI_API_KEY

def lambda_handler(event, context):
    documents = SimpleDirectoryReader(input_dir="./data").load_data()
    print("documents: ", documents)
    list_index = GPTListIndex.from_documents(documents)
    print("list_index: ", list_index)
    query_engine = list_index.as_query_engine()
    print("query_engine: ", query_engine)
    response = query_engine.query("機械学習に関するアップデートについて300字前後で要約してください。")
    print("response: ", response)

    return {
        "statusCode": 200,
        "body": json.dumps(
            {
                "message": "hello world",
            }
        ),
    }

import json
import os
import boto3
import openai

from dotenv import load_dotenv
from langchain import OpenAI
from llama_index import VectorStoreIndex, SimpleDirectoryReader
from llama_index import StorageContext, load_index_from_storage

from dotenv import load_dotenv
load_dotenv()
API_KEY_ENV_NAME = 'API_Key'
OPENAI_API_KEY = os.environ[API_KEY_ENV_NAME]
openai.api_key = OPENAI_API_KEY

def lambda_handler(event, context):
    # モデルの読み込み
    storage_context = StorageContext.from_defaults(persist_dir='./storage')
    index = load_index_from_storage(storage_context)

    # イベントからメッセージを取得
    try:
        message = json.loads(event['body'])['message']
    except KeyError:
        return {
            "statusCode": 400,
            "body": json.dumps({
                "message": "Invalid input. 'message' key is required."
            })
        }

    # クエリの実行
    query_engine = index.as_query_engine()
    response = query_engine.query(message)
    print("response: ", response)
    response = str(response)

    return {
        "statusCode": 200,
        "body": json.dumps(
            {
                "message": response,
            }
        ),
    }

import json
import os
import boto3
import openai

from dotenv import load_dotenv
from langchain import OpenAI
from llama_index import VectorStoreIndex, SimpleDirectoryReader
from llama_index import StorageContext, load_index_from_storage

load_dotenv()
API_KEY_ENV_NAME = 'API_Key'
OPENAI_API_KEY = os.getenv(API_KEY_ENV_NAME)
openai.api_key = OPENAI_API_KEY

def get_message_from_event(event):
    try:
        return json.loads(event['body'])['input_text']
    except KeyError:
        raise ValueError("Invalid input. 'message' key is required.")

def generate_error_response(message):
    return {
        "statusCode": 400,
        "body": json.dumps({
            "message": message
        })
    }

def generate_success_response(response):
    return {
        "statusCode": 200,
        "body": json.dumps({
            "Response": str(response),
        }),
    }

def lambda_handler(event, context):
    try:
        message = get_message_from_event(event)
    except ValueError as error:
        return generate_error_response(str(error))

    storage_context = StorageContext.from_defaults(persist_dir='./storage')
    index = load_index_from_storage(storage_context)
    query_engine = index.as_query_engine()

    response = query_engine.query(message)
    print("response: ", response)

    return generate_success_response(response)

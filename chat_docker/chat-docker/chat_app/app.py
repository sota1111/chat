import json
import os
import boto3
import openai
from dotenv import load_dotenv
from langchain import OpenAI
from llama_index import VectorStoreIndex, SimpleDirectoryReader
from llama_index import StorageContext, load_index_from_storage

from botocore.exceptions import ClientError

def get_secret():

    secret_name = "openai"
    region_name = "ap-northeast-1"

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        # For a list of exceptions thrown, see
        # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
        raise e

    # Decrypts secret using the associated KMS key.
    secret = get_secret_value_response['SecretString']
    key_value = json.loads(secret)
    openai.api_key = key_value['openai']    

# イベントからメッセージを取得
def get_message_from_event(event):
    try:
        return json.loads(event['body'])['input_text']
    except KeyError:
        raise ValueError("Invalid input. 'input_text' key is required.")

# エラーレスポンス関数
def generate_error_response(message):
    return {
        "statusCode": 400,
        "body": json.dumps({
            "message": message
        })
    }

# 成功レスポンス関数
def generate_success_response(response):
    return {
        "statusCode": 200,
        "body": json.dumps({
            "Response": str(response),
        }),
    }

# Lambdaハンドラー関数
def lambda_handler(event, context):

    get_secret()

    try:
        message = get_message_from_event(event)
    except ValueError as error:
        return generate_error_response(str(error))

    # indexの読み込み
    storage_context = StorageContext.from_defaults(persist_dir='./storage')
    index = load_index_from_storage(storage_context)

    # クエリの実行
    query_engine = index.as_query_engine()
    response = query_engine.query(message)
    #response = 'hello world'
    print("response: ", response)

    return generate_success_response(response)

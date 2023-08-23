import json
import os
import boto3
import openai
from dotenv import load_dotenv

from botocore.exceptions import ClientError
from config import DYNAMODB_TABLE_NAME
from utils import get_max_conversation_id, get_chat_response_func, get_chat_response, store_conversation, delete_items_with_secondary_index, create_function_args
from role.role_tetris import get_chat_messages_tetris, get_chat_functions_tetris, search_tetris_index#evalで参照

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
    body_content = event.get('body', None)
    
    if not body_content:
        raise ValueError("The 'body' field in the event is missing or empty.")
    
    try:
        return json.loads(body_content)['input_text']
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
    # HTTPメソッドがGETの場合、"hello world"を返す
    http_method = event.get('httpMethod', '')
    if http_method == 'GET':
        return generate_success_response('hello world')
    elif http_method == 'PUT':#処理はDeleteだが、bodyを取るので、Put methodで定義
        try:
            data = json.loads(event["body"])
            user_id = data['identity_id']
            char_name = data['character_name']
            delete_items_with_secondary_index(user_id, char_name)
            return {
                    'statusCode': 200,
                    'body': json.dumps({
                        'message': 'Delete operation completed',
                    }),
                    'headers': {
                        'Content-Type': 'application/json',
                        'Access-Control-Allow-Origin': '*',
                        'Access-Control-Allow-Credentials': True,
                    },
                }
        except Exception as e:
            print(f"An error occurred: {e}")
            return {
                'statusCode': 500,
                'body': json.dumps({
                    'message': f'Error during delete operation: {e}',
                }),
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Credentials': True,
                },
            }


    elif http_method == 'POST':
        data = json.loads(event["body"])
        user_id = data['identity_id']
        char_name = data['character_name']
        input_text = data['input_text']
        get_secret()
        # メッセージを取得
        try:
            message = get_message_from_event(event)
        except ValueError as error:
            return generate_error_response(str(error))
        
        # GPT API動作 ここにfunctionありのapiを実装する
        # 過去の応答を取得
        messages = get_chat_messages_tetris()
        functions = get_chat_functions_tetris() #最初はfunction機能は使わない
        max_order_id,items = get_max_conversation_id(user_id, char_name)
        #今までの対話をmessagesに並べる
        messages.extend([{"role": item["role"], "content": item["content"]} for item in items])
        messages.append({"role": "user", "content": data['input_text']})
        #openAIのAPIを叩く
        if(0):
            response = get_chat_response(messages)
            response_content = response["choices"][0]["message"]["content"]
        else:
            response_1st = get_chat_response_func(messages, functions)
            response_data = response_1st["choices"][0]
            if response_data["finish_reason"] == "function_call":
                if response_data["message"]["function_call"]["name"]:
                    # 関数名や引数を取得する
                    call_data = response_data["message"]["function_call"]
                    func_name = call_data["name"]
                    args = eval(call_data["arguments"])
                    print(f"func_name: {func_name}, args: {args}")
                    # 選択された関数を実行
                    func = globals()[func_name]
                    function_response = func(**args)
                    print(f"function_response: {function_response}")

                    # 2回目のAPI実行
                    function_args = create_function_args(func_name, args)
                    print(f"function_args: {function_args}")
                    messages.append({"role": "assistant", "content": None, "function_call": function_args})
                    messages.append({"role": "function", "name": func_name, "content": function_response})
                    #print(f"messages: {messages}")

                    response_2nd = get_chat_response_func(messages, functions)
                    response_content = response_2nd.choices[0]["message"]["content"]

                    # DynamoDBにトーク履歴を記録
                    store_conversation(user_id, char_name, max_order_id, input_text, "user")
                    store_conversation(user_id, char_name, max_order_id + 1, None, "function")
                    store_conversation(user_id, char_name, max_order_id + 2, response_content, "assistant")

        return generate_success_response(response_content)
    



import json
import boto3
from config import DYNAMODB_TABLE_NAME
from utils import get_max_conversation_id, get_chat_response_func, get_chat_response, store_conversation, decimal_to_int, delete_items_with_secondary_index
from role.role_dio import get_chat_messages_dio, get_chat_functions_dio, process_response_message_dio
from role.role_heiji import get_chat_messages_heiji, get_chat_functions_heiji, process_response_message_heiji
from role.role_conan import get_chat_messages_conan, get_chat_functions_conan, process_response_message_conan
import re

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(DYNAMODB_TABLE_NAME)

    data = json.loads(event["body"])
    user_id = data['userid']
    conv_id = data['convid']
    print('conv_id:', conv_id)
    print('user_id:', user_id)
    

    if data.get('method') == "Delete":
        try:
            print('''data['method']:''', data['method'])
            delete_items_with_secondary_index(user_id, conv_id)
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
            
    
    # chatGPTに送信する文字列を生成
    if conv_id == "Dio":
        messages = get_chat_messages_dio()
        functions = get_chat_functions_dio()
    elif conv_id == "Heiji":
        messages = get_chat_messages_heiji()
    elif conv_id == "Conan":
        messages = get_chat_messages_conan()
        
    if data.get('system') == "true":
        role = 'system'
    else:
        role = 'user'
    print('role:', role)
    
    # 過去の応答を取得
    max_chat_id,items = get_max_conversation_id(table, user_id, conv_id)
    print('max_chat_id:', max_chat_id)
    for item in items:
        chat_content = item["content"]
        chat_role = item["role"]
        messages.append({"role": chat_role, "content": chat_content})
    input_text = data['input_text']
    messages.append({"role": role, "content": input_text})
    print('conv_id:', conv_id)
    print('user_id:', user_id)
    
    # chatGPTに文字列を送信
    if data.get('response_necessary') == "false":
        content = ""
        quote = "false"
        quote_num ="0"
        url = "None"
        store_conversation(table, user_id, conv_id, max_chat_id, input_text, role)
    else:
        if conv_id == "Dio":
            response = get_chat_response_func(messages, functions)
        elif conv_id == "Heiji":
            response = get_chat_response(messages)
        elif conv_id == "Conan":
            response = get_chat_response(messages)
        
        chat_response = json.dumps(response, default=decimal_to_int, ensure_ascii=False)
        chat_dict = json.loads(chat_response)
        
        # 応答を取得
        if conv_id == "Dio":
            content, quote, quote_num, url = process_response_message_dio(response)
        elif conv_id == "Heiji":
            content, quote, quote_num, url = process_response_message_heiji(response)
        elif conv_id == "Conan":
            content, quote, quote_num, url = process_response_message_conan(response)
            
        # DynamoDBにトーク履歴を記録
        store_conversation(table, user_id, conv_id, max_chat_id, input_text, role)
        store_conversation(table, user_id, conv_id, max_chat_id + 1, content, 'assistant')
        

    print('input_text:', input_text)
    print('content:', content)
    
    # クライアントにデータを渡す
    return_json = {
        'statusCode': 200,
        'body': json.dumps({
            'Response': content,
            "Quote": quote,
            "Url":url,
        }),
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Credentials': True,
        },
    }
    
    return return_json
import boto3
import openai
import json
from decimal import Decimal
from config import DYNAMODB_TABLE_NAME, DYNAMODB_INDEX_NAME, OPENAI_API_KEY, OPENAI_MODEL_NAME
import re
from boto3.dynamodb.conditions import Key

openai.api_key = OPENAI_API_KEY

def decimal_to_int(obj):
    return int(obj) if isinstance(obj, Decimal) else obj

def get_max_conversation_id(table, user_id, conv_id):
    response = table.query(
        IndexName=DYNAMODB_INDEX_NAME,
        KeyConditionExpression=Key('userid').eq(user_id) & Key('convid').eq(conv_id),
        ScanIndexForward=False
    )
    items = response.get('Items', [])
    #print('items:', items)
    max_chat_id = max(item['chatid'] for item in items) if items else -1
    return max_chat_id, items

def delete_items_with_secondary_index(user_id, conv_id):
    # Create a DynamoDB client
    client = boto3.client('dynamodb')

    # Query the index
    response = client.query(
        TableName=DYNAMODB_TABLE_NAME,
        IndexName=DYNAMODB_INDEX_NAME,
        KeyConditionExpression='userid = :uid and convid = :cid',
        ExpressionAttributeValues={
            ':uid': {'S': user_id},
            ':cid': {'S': conv_id},
        },
    )

    primary_keys = [{'userid': item['userid'], 'chatid': item['chatid']} for item in response['Items']]

    # Delete items using primary keys
    for key in primary_keys:
        print('delete_item:', key)
        client.delete_item(TableName=DYNAMODB_TABLE_NAME, Key=key)

    print(f'Deleted {len(primary_keys)} item(s) from {DYNAMODB_TABLE_NAME}.')


    
def get_chat_response(messages):
    return openai.ChatCompletion.create(
        model=OPENAI_MODEL_NAME,
        messages=messages,
        #max_tokens=500,
        #n=1,
        #temperature=0.5
    )

def get_chat_response_func(messages, functions):
    return openai.ChatCompletion.create(
        model=OPENAI_MODEL_NAME,
        messages=messages,
        functions=functions,
        function_call="auto",  # auto is default, but we'll be explicit optional
        #max_tokens=500,
        #n=1,utio
        #temperature=0.5
    )

def store_conversation(table, user_id, conv_id, max_chat_id, content, role):
    """Store conversation in DynamoDB."""
    item = {
        'userid': user_id,
        'chatid': (max_chat_id + 1),
        'convid': conv_id,
        'content': content,
        'role': role
    }
    table.put_item(Item=item)
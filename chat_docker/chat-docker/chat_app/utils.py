import boto3
import openai
import json
from decimal import Decimal
from config import DYNAMODB_TABLE_NAME, DYNAMODB_INDEX_NAME, OPENAI_MODEL_NAME
import re
from boto3.dynamodb.conditions import Key

def decimal_to_int(obj):
    return int(obj) if isinstance(obj, Decimal) else obj

def get_max_conversation_id(user_id, char_name):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(DYNAMODB_TABLE_NAME)
    response = table.query(
        IndexName=DYNAMODB_INDEX_NAME,
        KeyConditionExpression=Key('user_id').eq(user_id) & Key('char_name').eq(char_name),
        ScanIndexForward=False
    )
    items = response.get('Items', [])
    #print('items:', items)
    max_order_id = max(item['order_id'] for item in items) if items else -1
    return max_order_id, items

def delete_items_with_secondary_index(user_id, char_name):
    client = boto3.client('dynamodb')

    # Query the index
    response = client.query(
        TableName=DYNAMODB_TABLE_NAME,
        IndexName=DYNAMODB_INDEX_NAME,
        KeyConditionExpression='user_id = :user_id and char_name = :cname',
        ExpressionAttributeValues={
            ':uid': {'S': user_id},
            ':cname': {'S': char_name},
        },
    )

    primary_keys = [{'user_id': item['user_id'], 'char_name': item['char_name']} for item in response['Items']]

    # Delete items using primary keys
    for key in primary_keys:
        print('delete_item:', key)
        client.delete_item(TableName=DYNAMODB_TABLE_NAME, Key=key)

    print(f'Deleted {len(primary_keys)} item(s) from {DYNAMODB_TABLE_NAME}.')


    
def get_chat_response(messages):
    response = openai.ChatCompletion.create(
        model=OPENAI_MODEL_NAME,
        messages=messages,
        #max_tokens=500,
        #n=1,
        #temperature=0.5
    )
    content = response["choices"][0]["message"]["content"]
    return content

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

def store_conversation(user_id, char_name, max_order_id, content, role):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(DYNAMODB_TABLE_NAME)
    """Store conversation in DynamoDB."""
    item = {
        'user_id': user_id,
        'order_id': (max_order_id + 1),
        'char_name': char_name,
        'content': content,
        'role': role
    }
    table.put_item(Item=item)
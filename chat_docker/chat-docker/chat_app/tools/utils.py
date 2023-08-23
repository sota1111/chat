import boto3
import openai
import json
from tools.config import DYNAMODB_TABLE_NAME, DYNAMODB_INDEX_NAME, OPENAI_MODEL_NAME
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key

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
    return response

def get_chat_response_func(messages, functions):
    response = openai.ChatCompletion.create(
        model=OPENAI_MODEL_NAME,
        messages=messages,
        functions=functions,
        function_call="auto",  # auto is default, but we'll be explicit optional
        #max_tokens=500,
        #n=1,utio
        #temperature=0.5
    )
    return response    

def store_conversation(user_id, char_name, max_order_id, role, content, name=None, function_call=None):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(DYNAMODB_TABLE_NAME)
    """Store conversation in DynamoDB."""
    item = {
        'user_id': user_id,
        'order_id': (max_order_id + 1),
        'char_name': char_name,
        'role': role,
        'content': content
    }
    
    if name:  # nameが存在している（None以外）場合
        item['name'] = name
    if function_call:  # function_callが存在している（None以外）場合
        item['function_call'] = function_call
        
    table.put_item(Item=item)


def create_function_args(func_name, args):
    function_call = {
        "name": func_name,
        "arguments": json.dumps(args)
    }
    return function_call
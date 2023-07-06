import os

DYNAMODB_TABLE_NAME = 'chatLog'
API_KEY_ENV_NAME = 'API_Key'
OPENAI_API_KEY = os.environ[API_KEY_ENV_NAME]
OPENAI_MODEL_NAME = "gpt-3.5-turbo-0613"#gpt-3.5-turbo-0613"
DYNAMODB_INDEX_NAME = 'userid-convid-index'
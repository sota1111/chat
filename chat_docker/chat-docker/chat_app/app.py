import json
from tools.utils import get_max_conversation_id, get_chat_response_func, get_chat_response, store_conversation, delete_items_with_secondary_index, create_function_args, get_secret
from tools.response import generate_success_response, generate_redirect_response, generate_client_error_response, generate_server_error_response
from role.role_tetris import get_chat_messages_tetris, get_chat_functions_tetris, search_tetris_index#evalで参照

# イベントからメッセージを取得
def get_message_from_event(event):
    body_content = event.get('body', None)
    
    if not body_content:
        raise ValueError("The 'body' field in the event is missing or empty.")
    
    try:
        return json.loads(body_content)['input_text']
    except KeyError:
        raise ValueError("Invalid input. 'input_text' key is required.")

def handle_get_request():
    return generate_success_response('hello world')

def handle_put_request(event):
    try:
        data = json.loads(event["body"])
        user_id = data['identity_id']
        char_name = data['character_name']
        try:
            delete_items_with_secondary_index(user_id, char_name)
            return generate_success_response('delete success')
        except:
            print(f"An error occurred: {e}")
            return generate_server_error_response(f'Error during delete operation: {e}')
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return generate_client_error_response(f'Error during delete operation: {e}')

def handle_post_request(event):
    get_secret()

    # メッセージを取得
    try:
        get_message_from_event(event)
        data = json.loads(event["body"])
        user_id = data['identity_id']
        char_name = data['character_name']
        input_text = data['input_text']
    except ValueError as e:
        return generate_client_error_response(f'Error during delete operation: {e}')
    
    # 過去の応答を取得
    messages = get_chat_messages_tetris()
    functions = get_chat_functions_tetris()
    max_order_id,items = get_max_conversation_id(user_id, char_name)

    #今までの対話をmessagesに並べる
    messages.extend([
        {
            "role": item["role"],
            "content": item["content"],
            **({"name": item["name"]} if "name" in item else {}),
            **({"function_call": item["function_call"]} if "function_call" in item else {})
        } 
        for item in items
    ])
    messages.append({"role": "user", "content": data['input_text']})
    
    #openAIのAPIを叩く
    if(0):#function callを使わない場合
        response = get_chat_response(messages)
        response_content = response["choices"][0]["message"]["content"]
        store_conversation(user_id, char_name, max_order_id + 0, "user", input_text)
        store_conversation(user_id, char_name, max_order_id + 1, "assistant", response_content)
    else:
        response_1st = get_chat_response_func(messages, functions)
        response_data = response_1st["choices"][0]
        if response_data["finish_reason"] == "function_call":
            print(f"function call defined\n")
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
                messages.append({"role": "function", "content": function_response, "name": func_name})
                #print(f"messages: {messages}")

                response_2nd = get_chat_response_func(messages, functions)
                response_content = response_2nd.choices[0]["message"]["content"]

                # DynamoDBにトーク履歴を記録 #store_conversation(user_id, char_name, max_order_id, role, content, name=None, function_call=None):
                store_conversation(user_id, char_name, max_order_id + 0, "user", input_text)
                store_conversation(user_id, char_name, max_order_id + 1, "assistant", None, name=None, function_call=function_args)
                store_conversation(user_id, char_name, max_order_id + 2, "function", function_response, name=func_name, function_call=None)
                store_conversation(user_id, char_name, max_order_id + 3, "assistant", response_content)

        else:
            print(f"function call undefined\n")
            response_content = response_1st["choices"][0]["message"]["content"]
            store_conversation(user_id, char_name, max_order_id + 0, "user", input_text)
            store_conversation(user_id, char_name, max_order_id + 1, "assistant", response_content)

# Lambdaハンドラー関数
def lambda_handler(event, context):
    http_method = event.get('httpMethod', '')
    if http_method == 'GET':
        return handle_get_request()
    elif http_method == 'PUT':
        return handle_put_request(event)
    elif http_method == 'POST':
        return handle_post_request(event)

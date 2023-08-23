import json

# 成功レスポンス関数
def generate_success_response(response):
    return {
        "statusCode": 200,
        "body": json.dumps({
            "Response": str(response),
        }),
    }
# リダイレクト関数
def generate_redirect_response(message):
    return {
        "statusCode": 300,
        "body": json.dumps({
            "message": message
        })
    }
# クライアントエラーレスポンス関数
def generate_client_error_response(message):
    return {
        "statusCode": 400,
        "body": json.dumps({
            "message": message
        })
    }
# サーバーエラーレスポンス関数
def generate_server_error_response(message):
    return {
        "statusCode": 500,
        "body": json.dumps({
            "message": message
        })
    }
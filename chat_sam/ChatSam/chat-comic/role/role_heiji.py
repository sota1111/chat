import json

def get_chat_messages_heiji():
    return [{"role": "system","content":
        
"""
名探偵コナンの登場人物"服部平次"の役を演じて。
"平次"は高校生探偵の"工藤新一"と関西弁で敬語を使わずに会話する。
以後の会話では、以下に従うこと。
・返答は30文字以内で回答する
・ステップバイステップで推理し、問いに対して１ステップを回答する
・一問一答で回答する
・###性格及び性格形成に関する記述###に基づいて回答する
・###平次の枕詞###を枕詞にできる時があれば、枕詞を付けて回答する
###平次の枕詞###
・工藤に話しかける時：「せやかて、工藤。」
・工藤の推理を聞いた時：「なんでや、工藤。理由を教えてくれ。」
・事件の核心に気がついた時：「もろたで、工藤。」
###性格及び性格形成に関する記述###
・勝ち負けにこだわる負けず嫌いな性格
・義理堅い
・短気で喧嘩っ早く、気にさわることをした者にすぐ怒鳴ったり絡んだりする。・黒ずくめの組織殲滅のために戦う意志を示す。
・和葉に対して一途に思っているが、その感情を表に出さない
"""
        },
    ]

def get_chat_functions_heiji():
    return [
        {
            "name": "get_quote",
            "description": "description",
            "parameters": {
                "type": "object",
                "properties": {
                    "QuoteNumber": {
                        "type": "string",
                        "description": "引用番号 e.g. 2",
                    },
                },
                "required": ["QuoteNumber"],
            },
        }
    ]
    
def process_response_message_heiji(response):
    quote = "false"
    quote_num ="0"
    url = "None"
    content = response['choices'][0]['message']['content']
    return content, quote, quote_num, url
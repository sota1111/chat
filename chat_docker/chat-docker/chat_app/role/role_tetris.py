import json

def get_chat_messages_tetris():
    return [{"role": "system","content":
        
"""
テトリスのルール解説をしてください。質問には100文字以内で回答してください。
"""
        },
        {"role": "user","content":"テトリスのルールを教えて。"},
        {"role": "assistant","content": "テトリスは、異なる形のブロックを落としてきて、行を埋めるゲームです。行を完全に埋めると、その行は消えます。ブロックが画面上部に積み上げられるとゲームオーバーです。"},
    ]

def get_chat_functions_tetris():
    return [
        {
            "name": "get_quote",
            "description": 
"""
テトリス対戦に関する情報を検索する関数。文脈が分からなかった場合、この関数を実行する。
""",
            "parameters": {
                "type": "object",
                "properties": {
                    "SearchContent": {
                        "type": "string",
                        "description": "テトリス対戦に関する情報を検索 e.g.ミノを消した時の点数は？",
                    },
                },
                "required": ["QuoteNumber"],
            },
        }
    ]
    

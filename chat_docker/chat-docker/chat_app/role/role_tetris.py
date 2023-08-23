import json
from langchain import OpenAI
from llama_index import VectorStoreIndex, SimpleDirectoryReader
from llama_index import StorageContext, load_index_from_storage

def get_chat_messages_tetris():
    return [{"role": "system","content":
        
"""
質問には100文字以内で回答する。
テトリス対戦のルール解説や文脈のない内容を聞かれた場合、"function"を実行する。
"function"の応答を用いて、"user"の言語に合わせた言語で100文字以内で回答する。
"""
        },
        {"role": "user","content":"テトリスのルールを教えて。"},
        {"role": "assistant","content": "テトリスは、異なる形のブロックを落としてきて、行を埋めるゲームです。行を完全に埋めると、その行は消えます。ブロックが画面上部に積み上げられるとゲームオーバーです。"},
    ]

def get_chat_functions_tetris():
    return [
        {
            "name": "search_tetris_index",
            "description": 
"""
テトリス対戦に関する情報を検索する関数。文脈が分からなかった場合、この"function"を実行する。
""",
            "parameters": {
                "type": "object",
                "properties": {
                    "SearchContent": {
                        "type": "string",
                        "description": "テトリス対戦に関する情報を検索 e.g.ミノを消した時の点数は？",
                    },
                },
                "required": ["SearchContent"],
            },
        }
    ]
    
def search_tetris_index(SearchContent):
    # indexの読み込み
    storage_context = StorageContext.from_defaults(persist_dir='./storage')
    index = load_index_from_storage(storage_context)

    # クエリの実行
    query_engine = index.as_query_engine()
    response = query_engine.query(SearchContent)

    result = {
        "response": response.response,
    }
    return json.dumps(result)

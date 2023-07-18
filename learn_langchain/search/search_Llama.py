import os
from llama_index import GPTVectorStoreIndex, SimpleDirectoryReader
import logging
import sys

from dotenv import load_dotenv
load_dotenv()

# ログレベルの設定
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG, force=True)



# インデックスの作成
documents = SimpleDirectoryReader("data").load_data()
index = GPTVectorStoreIndex.from_documents(documents)
import os
from langchain.llms import OpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.schema import (
    SystemMessage,
    HumanMessage,
)
# 環境変数の設定
from dotenv import load_dotenv
load_dotenv()

# LLMsの使い方
llm = OpenAI(model_name="text-davinci-003")
response = llm("ITエンジニアについて30文字で教えて。")
print(response)

# Chat Modelsの使い方
chat = ChatOpenAI(model_name="gpt-3.5-turbo")
response = chat([
	SystemMessage(content="日本語で回答して。"),
	HumanMessage(content="ITエンジニアについて30文字で教えて。"),
])
print(response.content)

# Embeddingsの使い方
embeddings = OpenAIEmbeddings()
query_result = embeddings.embed_query("ITエンジニアについて30文字で教えて。")
print(query_result)
print(len(query_result))
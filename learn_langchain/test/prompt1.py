import os
from langchain import PromptTemplate
from langchain import FewShotPromptTemplate
from langchain.llms import OpenAI

from langchain.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.chat_models import ChatOpenAI

from dotenv import load_dotenv
load_dotenv()

# Prompt Templateの使い方
template = """
{subject}について30文字で教えて。
"""

prompt = PromptTemplate(
		template=template,
    input_variables=["subject"]
)
prompt_text = prompt.format(subject="ITエンジニア")
print(prompt_text)

llm = OpenAI(model_name="text-davinci-003")
print(llm(prompt_text) + "\n\n")

# Few Shot Prompt Templateの使い方
examples = [
    {"fruit": "りんご", "color": "赤"},
    {"fruit": "キウイ", "color": "緑"},
    {"fruit": "ぶどう", "color": "紫"},
]

example_formatter_template = """
フルーツ: {fruit}
色: {color}\n
"""
example_prompt = PromptTemplate(
    template=example_formatter_template,
    input_variables=["fruit", "color"]
)

few_shot_prompt = FewShotPromptTemplate(
    examples=examples,
    example_prompt=example_prompt,
    prefix="フルーツの色を漢字で教えて。",
    suffix="フルーツ: {input}\n色:",
    input_variables=["input"],
    example_separator="\n\n",
)

prompt_text = few_shot_prompt.format(input="オレンジ")
print(prompt_text + "\n\n")

llm = OpenAI(model_name="text-davinci-003")
print(llm(prompt_text))

# Chat Prompt Templateの使い方
system_template="あなたは、質問者からの質問を{language}で回答するAIです。"
human_template="質問者：{question}"
system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)
human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)

chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])
prompt_message_list = chat_prompt.format_prompt(language="日本語", question="ITエンジニアについて30文字で教えて。").to_messages()

print(prompt_message_list)

chat = ChatOpenAI(model_name="gpt-3.5-turbo")
response = chat(prompt_message_list)
print(response)

# Example Selectorsの使い方
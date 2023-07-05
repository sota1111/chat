from langchain.output_parsers import CommaSeparatedListOutputParser
from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI

from dotenv import load_dotenv
load_dotenv()

# Output Parsersの使い方
output_parser = CommaSeparatedListOutputParser()
format_instructions = output_parser.get_format_instructions()
prompt = PromptTemplate(
    template="List five {subject}.\n{format_instructions}",
    input_variables=["subject"],
    partial_variables={"format_instructions": format_instructions}
)

llm = OpenAI(model_name="text-davinci-003")
_input = prompt.format(subject="Programming Language")
output = llm(_input)
response = output_parser.parse(output)
print(response)

from typing import List
from pydantic import BaseModel, Field

from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI
from langchain.output_parsers import PydanticOutputParser

class Job(BaseModel):
    name: str = Field(description="Name of the job")
    skill_list: List[str] = Field(description="List of skills required for that job")

parser = PydanticOutputParser(pydantic_object=Job)
prompt = PromptTemplate(
    template="{query}\n\n{format_instructions}\n",
    input_variables=["query"],
    partial_variables={"format_instructions": parser.get_format_instructions()}
)
_input = prompt.format_prompt(query="Tell me the skills required for frontend engineer.")
print("_input:",_input)

llm = OpenAI(model_name="text-davinci-003")
output = llm(_input.to_string())
print("output:",output)


print("parser.parse(output):")
parser.parse(output)
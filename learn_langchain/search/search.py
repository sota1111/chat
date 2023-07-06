from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import PyPDFLoader
import pickle
from dotenv import load_dotenv
load_dotenv()

loader = PyPDFLoader("https://chat-tetris.s3.ap-northeast-1.amazonaws.com/seigot_tetris.pdf")
documents = loader.load()

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
texts = text_splitter.split_documents(documents)
#print("texts:",texts)

embeddings = OpenAIEmbeddings()
vectordb = Chroma.from_documents(texts, embeddings)
#print("vectordb:",vectordb)

qa = RetrievalQA.from_chain_type(
    llm=ChatOpenAI(model_name="gpt-3.5-turbo",temperature=0),
    chain_type="stuff", # default: "stuff"
    retriever=vectordb.as_retriever()
)
response = qa.run("テトリスアートに関して教えて。")
print("response:",response)
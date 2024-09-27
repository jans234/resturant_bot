import os
from tqdm import tqdm
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
import shutil
load_dotenv()

def loader(fast=False):
    embeddings = OpenAIEmbeddings()
    if os.path.exists("./chromadb"):
        shutil.rmtree("./chromadb")
    vectorstore = Chroma(
        persist_directory="./chromadb",
        embedding_function=embeddings,
        collection_name="meals"
        )
    root_path = './dataset'
    items = os.listdir(root_path)
    if not fast:
        for i in tqdm(items):
            with open(f"{root_path}/{i}",'r', encoding='utf-8') as f:
                Chroma.add_texts(vectorstore, [f.read()])
    else:
        DOCUMENT = []
        for i in items:
            with open(f"{root_path}/{i}",'r', encoding='utf-8') as f:
                DOCUMENT.append(f.read())
        Chroma.add_texts(vectorstore, DOCUMENT)


    

def retriver(question:str):
    embeddings = OpenAIEmbeddings()
    vectorstore = Chroma(
        persist_directory="./chromadb",
        embedding_function=embeddings,
        collection_name="meals"
        )
    DOCS = []
    for i in vectorstore.similarity_search(question, k=4):
        print (vectorstore)
        DOCS.append(i.page_content)
    return DOCS

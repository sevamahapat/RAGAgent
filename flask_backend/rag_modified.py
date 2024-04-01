import os
from dotenv import load_dotenv,find_dotenv
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma

from langchain.llms import HuggingFacePipeline
from langchain.embeddings import HuggingFaceEmbeddings
load_dotenv(find_dotenv())

def load_document(file):
    from langchain.document_loaders import TextLoader
    loader = TextLoader(file)

    data = loader.load()
    return data

# splitting data in chunks
def chunk_data(data, chunk_size=1000, chunk_overlap=20):
    from langchain.text_splitter import RecursiveCharacterTextSplitter
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    chunks = text_splitter.split_documents(data)
    return chunks

# create embeddings using OpenAIEmbeddings() and save them in a Chroma vector store
def create_embeddings(chunks):
    embeddings = OpenAIEmbeddings()
    if os.environ.get('FLASK_ENV') == 'local':
        vector_store = Chroma.from_documents(documents=chunks, embedding=embeddings, persist_directory="chroma_db")
        vector_store.persist()
    elif os.environ.get('FLASK_ENV') == 'production':
        vector_store = Chroma(persist_directory="chroma_db", embedding_function = embeddings)

    return vector_store

def ask_and_get_answer(vector_store, q, k=3):
    from langchain.chains import RetrievalQA
    from langchain.chat_models import ChatOpenAI

    # llm = ChatOpenAI(model='gpt-3.5-turbo', temperature=0.1)
    llm = ChatOpenAI(model='gpt-4-1106-preview')
    # retriever = vector_store.as_retriever(search_type='similarity', search_kwargs={'k': k})
    retriever = vector_store.as_retriever()

    chain = RetrievalQA.from_chain_type(
        llm=llm, 
        chain_type="stuff", 
        retriever=retriever, 
        verbose=True
    )

    answer = chain.run(q)
    return answer

def generate_response(query):

    data = load_document("product_details.txt")
    chunks = chunk_data(data)

    # creating the embeddings and returning the Chroma vector store
    vector_store = create_embeddings(chunks)

    response = ask_and_get_answer(vector_store, query)

    return response
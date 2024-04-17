import streamlit as st
import os
from langchain_groq import ChatGroq
from langchain_community.document_loaders import WebBaseLoader
from langchain.embeddings import OllamaEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain
from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS

load_dotenv()

##load the groq api key

groq_api_key = os.environ['GROQ_API_KEY']

if "vectors" not in st.session_state:
    st.session_state.embeddings=OllamaEmbeddings()
    st.session_state.loader = WebBaseLoader("https://docs.smith.langchain.com/")
    st.session_state.docs = st.session_state.loader.load()
    st.session_state.text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    st.session_state.final_documents = st.session_state.text_splitter.split_documents(st.session_state.docs[:50])
    st.session_state.vectors = FAISS.from_documents(st.session_state.final_documents, st.session_state.embeddings)
    
st.title("ChatGroq Demo")
llm = ChatGroq(groq_api_key=groq_api_key, model_name ="mixtral-8x7b-32768")
prompts = ChatPromptTemplate.from_template(
    """
    Respond accurately based on the context.
    <context>
    {context}
    </context>
    Questions: {input}
    
    """
    )
document_chain = create_stuff_documents_chain(llm, prompts)
retriever = st.session_state.vectors.as_retriever()
retrieval_chain = create_retrieval_chain(retriever, document_chain)
prompt = st.text_input("Question")

if prompt:
    response = retrieval_chain.invoke({"input": prompt})
    st.write(response['answer'])
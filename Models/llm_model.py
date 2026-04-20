import streamlit as st
from langchain_ollama import ChatOllama
from langchain_ollama import OllamaEmbeddings


@st.cache_resource
def load_llm():

    llm = ChatOllama(
        model="llama3.2:1b",
        temperature=0
    )

    return llm


@st.cache_resource
def load_embeddings():

    embeddings = OllamaEmbeddings(
        model="nomic-embed-text"
    )

    return embeddings
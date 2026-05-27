import os
import streamlit as st

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_openai import OpenAIEmbeddings

load_dotenv()


@st.cache_resource
def load_llm():

    llm = ChatGroq(
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model_name="llama-3.3-70b-versatile",
    temperature=0
)

    return llm


@st.cache_resource
def load_embeddings():

    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small"
    )

    return embeddings
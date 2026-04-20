from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

from Backend.youtube_utils import get_transcript
from Models.llm_model import load_embeddings, load_llm
from Prompt.prompt_template import get_prompt


def create_vector_store(video_id):

    embeddings = load_embeddings()

    transcript = get_transcript(video_id)

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    docs = splitter.create_documents([transcript])

    vector_store = FAISS.from_documents(docs, embeddings)

    return vector_store


def build_rag_chain(vector_store):

    llm = load_llm()

    prompt = get_prompt()

    retriever = vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 2}
    )

    rag_chain = (
        {
            "context": retriever,
            "question": RunnablePassthrough()
        }
        | prompt
        | llm
        | StrOutputParser()
    )

    return rag_chain
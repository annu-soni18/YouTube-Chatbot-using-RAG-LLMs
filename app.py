import streamlit as st
import time

from Backend.youtube_utils import extract_youtube_id
from Backend.rag_pipeline import create_vector_store, build_rag_chain


st.set_page_config(
    page_title="YouTube Chatbot",
    page_icon="▶",
    layout="wide"
)

st.title("YouTube RAG Chatbot", text_alignment="center")
st.markdown("A RAG-based chatbot that understands and answers queries from YouTube videos.", text_alignment="center")

# session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "video_id" not in st.session_state:
    st.session_state.video_id = None

if "vector_store" not in st.session_state:
    st.session_state.vector_store = None

if "rag_chain" not in st.session_state:
    st.session_state.rag_chain = None


# -------- SIDEBAR --------

with st.sidebar:

    st.title("Load YouTube Video")

    url = st.text_input(
        "Paste YouTube URL",
        placeholder="https://youtu.be/..."
    )

    if st.button("Extract ID"):

        with st.spinner("Loading video..."):

            time.sleep(1)

            video_id = extract_youtube_id(url)

        if video_id:

            st.session_state.video_id = video_id

            with st.spinner("Preparing knowledge base..."):

                vector_store = create_vector_store(video_id)

                rag_chain = build_rag_chain(vector_store)

                st.session_state.vector_store = vector_store
                st.session_state.rag_chain = rag_chain

            st.success("Video ready for chat!")

        else:

            st.error("Invalid YouTube URL")


    if st.session_state.video_id:

        st.video(
            f"https://www.youtube.com/watch?v={st.session_state.video_id}"
        )

        if st.button("Clear Chat"):

            st.session_state.messages = []
            st.rerun()


# -------- CHAT HISTORY --------

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# -------- USER INPUT --------

question = st.chat_input("Ask anything about the video")


if question:

    if st.session_state.rag_chain:

        with st.chat_message("user", avatar="🧑"):
            st.markdown(question)

        st.session_state.messages.append(
            {"role": "user", "content": question}
        )

        with st.chat_message("assistant", avatar="🤖"):

            full_response = ""
            placeholder = st.empty()

            for chunk in st.session_state.rag_chain.stream(question):

                full_response += chunk
                placeholder.markdown(full_response)

        st.session_state.messages.append(
            {"role": "assistant", "content": full_response}
        )

    else:

        st.error("Please load a YouTube video first.")
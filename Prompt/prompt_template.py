from langchain_core.prompts import PromptTemplate


def get_prompt():

    prompt = PromptTemplate(
        template="""
You are a helpful assistant that answers questions about a YouTube video.

Answer ONLY using the provided context.

Context:
{context}

Question:
{question}
""",
        input_variables=["context", "question"]
    )

    return prompt
from langchain_core.prompts import PromptTemplate
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_ollama import ChatOllama
from dotenv import load_dotenv
import os

load_dotenv()


# 1. LLM
def get_llm_chain(retriever):
    llm=ChatOllama(
        model="llama3.1"
    )

    prompt=PromptTemplate(
        input_variables=["context", "input"],
        template="""
        You are **MediBot**, an AI-powered assistant trained to help users understand medical documents and health-related questions.

        Your job is to provide clear, accurate, and helpful responses based **only on the provided context**.

        ---

        🔍 **Context**:
        {context}

        🙋‍♂️ **User Question**:
        {input}

        ---

        💬 **Answer**:
        - Respond in a calm, factual, and respectful tone.
        - Use simple explanations when needed.
        - If the context does not contain the answer, say: "I'm sorry, but I couldn't find relevant information in the provided documents."
        - Do NOT make up facts.
        - Do NOT give medical advice or diagnoses.
        """
    )

    return create_retrieval_chain(
        retriever=retriever,
        combine_docs_chain=create_stuff_documents_chain(llm, prompt)
    )

    
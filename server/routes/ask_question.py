from fastapi import APIRouter, Form
from fastapi.responses import JSONResponse
from modules.llm import get_llm_chain
from modules.query_handlers import query_chain
from langchain_core.documents import Document
from langchain.schema import BaseRetriever
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from pinecone import Pinecone
from pydantic import Field
from typing import List, Optional
from logger import logger
import os

router = APIRouter()

class SimpleRetriever(BaseRetriever):
    docs: List[Document]

    def _get_relevant_documents(self, query: str) -> List[Document]:
        return self.docs

@router.post("/ask/")
async def ask_question(question: str = Form(...)):
    try:
        logger.info(f"User Query: {question}")
        
        # Pinecone and Embedding setup
        pinecone_api_key = os.getenv("PINECONE_API_KEY")
        google_api_key = os.getenv("GOOGLE_API_KEY")
        index_name = os.getenv("PINECONE_INDEX_NAME", "medical-index")

        pc = Pinecone(api_key=pinecone_api_key)
        index = pc.Index(index_name)
        
        embed_model = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=google_api_key)
        
        # Embed query and search Pinecone
        embedded_query = embed_model.embed_query(question)
        res = index.query(vector=embedded_query, top_k=3, include_metadata=True)

        docs = [
            Document(
                page_content=match["metadata"].get("text", ""),
                metadata=match["metadata"]
            )
            for match in res["matches"]
        ]

        # Initialize Retriever and Chain
        retriever = SimpleRetriever(docs=docs)
        chain = get_llm_chain(retriever)
        
        # Execute query
        result = query_chain(chain, question)

        logger.info("Query successful")
        return JSONResponse(content=result)
    
    except Exception as e:
        logger.exception(f"Error in ask_question: {e}")
        return JSONResponse(status_code=500, content={"error": str(e)})
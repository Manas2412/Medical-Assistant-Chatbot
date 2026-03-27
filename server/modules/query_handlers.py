from logger import logger
from fastapi import HTTPException

def query_chain(chain, user_input:str):
    try:
        logger.debug(f"User Input: {user_input}")
        result=chain.invoke({"input":user_input})
        response={
            "response":result["answer"],
            "sources":[doc.metadata.get("source","") for doc in result["context"]]
        }
        logger.debug(f"Response: {response}")
        return response
    except Exception as e:
        logger.error(f"Error in query_chain: {str(e)}")
        raise HTTPException(status_code=500,detail=f"Error: {str(e)}")